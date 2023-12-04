from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure

@allure.epic("Delete user cases")
class TestUserDelete(BaseCase):
    @allure.feature("Negative tests")
    @allure.title("Delete by unauthorized user")
    @allure.description("This test checks if we can delete data by unauthorized user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_user_not_auth(self):
        response = MyRequests.delete("/user/2")

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Auth token not supplied", \
            f"Unexpected response content {response.content}"

    @allure.feature("Positive tests")
    @allure.title("Delete by authorized user")
    @allure.description("In this test we create, login and delete user, and check that the user is deleted")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_user_successfully(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        # DELETE
        response3 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_code_status(response4, 404)
        assert response4.content.decode("utf-8") == f"User not found", \
            f"Unexpected response content {response4.content}"

    @allure.feature("Negative tests")
    @allure.title("Delete user by another user")
    @allure.description("This test checks if user can be deleted by another authorized user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_user_with_other_user_auth(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        # DELETE
        response3 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode("utf-8") == f"Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"Unexpected response content {response3.content}"