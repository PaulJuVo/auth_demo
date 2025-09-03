from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str


# nur für validierung
class TokenData(BaseModel):
    username: str | None = None