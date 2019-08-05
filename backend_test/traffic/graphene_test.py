import json

from graphene_django.utils.testing import GraphQLTestCase
from backend_test.traffic import schema
from django.core.management import call_command


class MyFancyTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def test_user_query(self):

        call_command('loaddata', 'FIXTURE/initial_data.json',
                     app_label='FIXTURE')
        response = self.query(
        ''' 
            query {
                   user(id:2) {
                   name
                  }
            }
        ''',
            op_name='user'
        )

        content = json.loads(response.content)
        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
        self.assertIsNotNone(content)

    def test_upsertUser_mutation(self):
        call_command('loaddata', 'FIXTURE/initial_data.json',
                     app_label='FIXTURE')
        response = self.query(
            '''
            mutation  {
              upsertUser (input: 
                {email: "dust.maximine@info.com.br",
                  name:"Dust",
                  dateOfBirth:"2098-06-29"}) {
                ok
                  user{ 
                    email
                  }
                }
            }
            ''',
            op_name='upsertUser',
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertIsNotNone(content)
