import httpx

from utils.parser import parser_response


class ProfileService:
    def __init__(self):
        self.base_url = "http://auth_service:8001"

    async def get_users_credentials(self, token: str) -> dict[str, str]:
        try:
            async with httpx.AsyncClient() as c:
                response = await c.get(
                    self.base_url + "/",
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=10.0,
                )
                if response.status_code != 200:
                    print(
                        f"error in getting user`s credentials by a GET handler {response.text}"
                    )
                    return dict()
                clear_data = parser_response(response.text)
                return clear_data["current user info"]

        except Exception as e:
            print(f"Failed to create account: {e}")
            return dict()
