import graphene
from graphene_django.types import DjangoObjectType
from .models import User, Website, Visit, Stats,Gender
from datetime import datetime
import graphene
from django.db.models import Max
from django.db.models import Q
GenderType = graphene.Enum.from_enum(Gender)
from django.db.models import Count

import graphene


class GenderType(graphene.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    UNIDENTIFIED = "UNIDENTIFIED"


class UserType(DjangoObjectType):
    class Meta:
        model = User


class WebsiteType(DjangoObjectType):
    class Meta:
        model = Website


class VisitType(DjangoObjectType):
    class Meta:
        model = Visit


class StatsType(DjangoObjectType):
    class Meta:
        model = Stats


class Query(object):
    user = graphene.Field(UserType,
                          id=graphene.Int(),
                          email=graphene.String())

    all_users = graphene.List(UserType)
    all_website = graphene.List(WebsiteType)
    website = graphene.Field(WebsiteType,
                             id=graphene.Int(),
                             url=graphene.String())

    all_visit = graphene.List(VisitType)

    users = graphene.List(UserType,
                          limit=graphene.Int(),
                          skip=graphene.Int(),
                          sort_field=graphene.String(),
                          sort_order=graphene.String())

    websites = graphene.List(WebsiteType,
                             limit=graphene.Int(),
                             skip=graphene.Int(),
                             sort_field=graphene.String(),
                             sort_order=graphene.String())

    statstotal = graphene.List(StatsType,
                                initial_timestamp=graphene.Date(),
                                final_timestamp =graphene.Date(),)

    statsbywebsite = graphene.List(StatsType,
                                initial_timestamp=graphene.Date(),
                                final_timestamp =graphene.Date(),)


    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_all_website(self, info, **kwargs):
        return Website.objects.all()

    def resolve_all_visit(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return Visit.objects.all()

    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')
        email = kwargs.get('email')

        if id is not None:
            return User.objects.get(pk=id)

        if email is not None:
            return User.objects.get(email=email)

        return None

    def resolve_website(self, info, **kwargs):
        id = kwargs.get('id')
        url = kwargs.get('url')

        if id is not None:
            return User.objects.get(pk=id)

        if url is not None:
            return User.objects.get(email=url)

        return None

    def resolve_statstotal(self, info, **kwargs):
        initial_timestamp = kwargs.get('initial_timestamp')
        final_timestamp = kwargs.get('final_timestamp')

        if initial_timestamp is None:
            initial_timestamp = datetime.min()
        if final_timestamp is None:
            final_timestamp = datetime.max()
        if final_timestamp and initial_timestamp is not None:
            s = Visit.objects.select_related(
                visit__timestamp_range=(initial_timestamp, final_timestamp))
        return s.stats.count()

    def resolve_statsbywebsite(self, info, **kwargs):
        return 0

    def resolve_users(self, info, **kwargs):
        limit = kwargs.get('limit')
        skip = kwargs.get('skip')
        sort_field = kwargs.get('sort_field')
        sort_order = kwargs.get('sort_order')
        if sort_order == "asc":
            sort_field = '-' + sort_field
        return User.objects.order_by(sort_field)[skip:limit]

    def resolve_websites(self, info, **kwargs):
        limit = kwargs.get('limit')
        skip = kwargs.get('skip')
        sort_field = kwargs.get('sort_field')
        sort_order = kwargs.get('sort_order')
        if sort_order == "asc":
            sort_field = '-' + sort_field
        return Website.objects.order_by(sort_field)[skip:limit]


# Create Input Object Types
class VisitInput(graphene.InputObjectType):
    website_url = graphene.ID()
    user_email = graphene.String()


class UserInput(graphene.InputObjectType):
    email = graphene.String()
    name = graphene.String()
    gender = graphene.Field(GenderType)
    date_of_birth = graphene.Date()


class WebsiteInput(graphene.InputObjectType):
    url = graphene.String()
    topic = graphene.String()


class UpsertWebsite(graphene.Mutation):
    class Arguments:
        input = WebsiteInput(required=True)

    ok = graphene.Boolean()
    website = graphene.Field(WebsiteType)

    @staticmethod
    def mutate(root, info, input=None):
        # Upserts a website.
        # If a website with the given url exists, update it.
        # Otherwise, create it.
        ok = False
        website, created =\
            Website.objects.get_or_create(url=input.url,
                                          defaults={'topic': input.topic})

        return UpsertWebsite(ok=ok, website=website)


class UpsertUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = False
        # Upserts a user.
        # If a user with the given email exists, update it.
        # Otherwise, create it.
        if input.gender is None:
            input.gender = Gender.UNIDENTIFIED
        user, created = User.objects.get_or_create(email=input.email,
            defaults = {'name': input.name,
                        'gender': input.gender,
                        'date_of_birth': input.date_of_birth})

        return UpsertUser(ok=ok, user=user)


class NewVisit(graphene.Mutation):
    class Arguments:
        input = VisitInput(required=True)

    ok = graphene.Boolean()
    visit = graphene.Field(VisitType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = False

        try:
            user_instance = User.objects.get(email=input.user_email)
        except User.DoesNotExist:
            return NewVisit(ok=ok, visit=None)
        try:
            website_instance = Website.objects.get(url=input.website_url)
        except Website.DoesNotExist:
            website_instance = None

        # If a website with the given url does not
        # exist in the database, create it.
        if website_instance is None:
            ok = True
            website_instance = Website(url=input.website_url)
            website_instance.save()
        # If a user with the given email does not
        # exist in the database, create it.
        if user_instance is None:
            user_instance = User(email=input.user_email)
            user_instance.save()

        # Records a new visit.
        visit_instance = Visit(website=website_instance,
                               user=user_instance)
        visit_instance.save()

        return NewVisit(ok=ok, visit=visit_instance)


class Mutation(graphene.ObjectType):
    newVisit = NewVisit.Field()
    upsertUser = UpsertUser.Field()
    upsertWebsite = UpsertWebsite.Field()


