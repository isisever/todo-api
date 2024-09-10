from marshmallow import Schema, fields


class TokenInfoSchema(Schema):
    Authorization = fields.String(required=True)

class LoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
