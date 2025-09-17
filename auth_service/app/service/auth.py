from uuid import UUID
import httpx


class AuthService:
    def __init__(self):
        self.base_url = "http://accounts_service:8002"

    async def create_account(self, user_id: UUID) -> str:
        try:
            async with httpx.AsyncClient() as c:
                account_data: dict[str, str | None] = {
                    "user_id": str(user_id),
                    "first_name": None,
                    "last_name": None,
                    "address": None,
                }
                response = await c.post(
                    self.base_url + "/profile", json=account_data, timeout=10.0
                )
                if response.status_code != 201:
                    print(
                        f"error when make creation of account in post handler {response.text}"
                    )
                    return ""
                return response.text.split('"')[3]

        except Exception as e:
            print(f"Failed to create account: {e}")
            return ""
