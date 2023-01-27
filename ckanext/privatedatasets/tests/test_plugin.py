"""
Tests for plugin.py.

Tests are written using the pytest library (https://docs.pytest.org), and you
should read the testing guidelines in the CKAN docs:
https://docs.ckan.org/en/2.9/contributing/testing.html

To write tests for your extension you should install the pytest-ckan package:

    pip install pytest-ckan

This will allow you to use CKAN specific fixtures on your tests.

For instance, if your test involves database access you can use `clean_db` to
reset the database:

    import pytest

    from ckan.tests import factories

    @pytest.mark.usefixtures("clean_db")
    def test_some_action():

        dataset = factories.Dataset()

        # ...

For functional tests that involve requests to the application, you can use the
`app` fixture:

    from ckan.plugins import toolkit

    def test_some_endpoint(app):

        url = toolkit.url_for('myblueprint.some_endpoint')

        response = app.get(url)

        assert response.status_code == 200


To temporary patch the CKAN configuration for the duration of a test you can use:

    import pytest

    @pytest.mark.ckan_config("ckanext.myext.some_key", "some_value")
    def test_some_action():
        pass
"""
import ckanext.privatedatasets.plugin as plugin
import ckanext.granularvisibility.plugin as plugin2
import ckan.plugins.toolkit as toolkit
from ckan import model

from ckan.tests import factories

import pytest


def test_plugin():
    pass

@pytest.mark.ckan_config('ckan.plugins', 'privatedatasets granularvisibility')
@pytest.mark.ckan_config("ckan.privatedatasets.parser", "ckanext.privatedatasets.parsers.fiware:FiWareNotificationParser")
@pytest.mark.usefixtures("with_plugins", "with_request_context")
@pytest.mark.usefixtures("clean_db")
class TestPrivateDatasets():
    def setup(self):
        # Create a dataset that will be used for testing
        self.admin = factories.User()
        self.owner_org = factories.Organization(users=[{
            'name': self.admin['name'],
            'id': self.admin['id'],
            'capacity': 'admin'
        }])
        self.dataset = factories.Dataset(private=True, owner_org=self.owner_org['id'], creator_user_id=self.admin["id"], user=self.admin )


        self.user = factories.User()
        pass

    ##############################
    ############ Auth ############
    ##############################

    # Test two users against package_show
    # Admin should have access
    # User shouldn't have access
    def test_auth_package_show(self):
        answer = plugin.auth.package_show({"user": self.admin["id"],"userobj": self.admin, "model": model}, self.dataset)
        answer2 = plugin.auth.package_show({"user": self.user["id"],"userobj": self.user, "model": model}, self.dataset)

        assert answer["success"] == True
        assert answer2["success"] == False

    ###############################
    ############# API #############
    ###############################

    def test_api_acquisitions_list(self):
        #Set user as an allowed user
        newMapping = plugin.db.AllowedUser()

        newMapping.package_id = self.dataset['id']
        newMapping.user_name = self.user["name"]
        newMapping.save()

        context = {'model': model, 'session': model.Session, 'ignore_auth': True}
        session = context['session']
        session.add(newMapping)
        session.commit()

        # Test the user acquisition_list
        data = {"user": self.user["name"]}
        acquisitions_list = plugin.actions.acquisitions_list(context,data)

        assert acquisitions_list == [self.dataset]

    def test_api_acquisitions_list_dataset(self):
        #Set user as an allowed user
        newMapping = plugin.db.AllowedUser()

        newMapping.package_id = self.dataset['id']
        newMapping.user_name = self.user["name"]
        newMapping.save()

        context = {'model': model, 'session': model.Session, 'ignore_auth': True}
        session = context['session']
        session.add(newMapping)
        session.commit()

        #Test the datasets allowed user list
        context = {'model': model, 'session': model.Session, 'ignore_auth': True}
        data = {"package_id": self.dataset["id"]}
        acquisitions_list_dataset = plugin.actions.acquisitions_list_dataset(context,data)

        assert acquisitions_list_dataset == [self.user["name"]]

    ################################
    ############ Helers ############
    ################################

    def test_helpers_is_dataset_acquired(self):
        #Set user as an allowed user
        newMapping = plugin.db.AllowedUser()

        newMapping.package_id = self.dataset['id']
        newMapping.user_name = self.user["name"]
        newMapping.save()

        context = {'model': model, 'session': model.Session, 'ignore_auth': True}
        session = context['session']
        session.add(newMapping)
        session.commit()

        # Check user is allowed
        plugin.tk.c.user = self.user["name"]
        assert plugin.helpers.is_dataset_acquired(self.dataset) == True

        # Check newUser is not allowed
        newUser = factories.User()
        plugin.tk.c.user = newUser["name"]
        assert plugin.helpers.is_dataset_acquired(self.dataset) == False

    def test_helpers_is_owner(self):
        
        # Check admin is a owner
        plugin.tk.c.userobj = model.User.get(self.admin["id"])
        assert plugin.helpers.is_owner(self.dataset) == True

        # Check newUser is not a owner
        newUser = factories.User()
        plugin.tk.c.userobj = model.User.get(newUser["id"])
        assert plugin.helpers.is_owner(self.dataset) == False

    def test_helpers_get_allowed_users_str(self):

        # Make sure None allowed users is displayed correctly
        assert plugin.helpers.get_allowed_users_str(self.dataset["id"]) == ""

        #Set user as an allowed user
        newMapping = plugin.db.AllowedUser()

        newMapping.package_id = self.dataset['id']
        newMapping.user_name = self.user["name"]
        newMapping.save()

        context = {'model': model, 'session': model.Session, 'ignore_auth': True}
        session = context['session']
        session.add(newMapping)
        session.commit()

        # Test the allowed user string is correct
        assert plugin.helpers.get_allowed_users_str(self.dataset["id"]) == "test_user_13"
