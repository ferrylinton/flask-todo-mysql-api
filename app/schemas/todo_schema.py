import arrow
from marshmallow import fields, validate, post_load, post_dump
from flask_jwt_extended import get_jwt_identity
from datetime import datetime
from .camel_case_schema import CamelCaseSchema

class TodoSchema(CamelCaseSchema):

    id = fields.Int(missing=0)
    task = fields.Str(validate=validate.Length(min=3, max=30, error="task min 3 chars and max 30 chars"))
    is_done = fields.Boolean(missing=False)
    created_by = fields.Str(dump_only=True)
    created_date = fields.Str(dump_only=True)
    last_modified_by = fields.Str(dump_only=True)
    last_modified_date = fields.Str(dump_only=True)
    current_user = fields.Str(dump_only=True)

    @post_load
    def make_object(self, data, **kwargs):
        utc = arrow.utcnow()
        current_user = get_jwt_identity()

        data['current_user'] = current_user
        data['created_by'] = current_user
        data['created_date'] = self.get_str_date(utc)
        data['last_modified_by'] = current_user
        data['last_modified_date'] = self.get_str_date(utc)
        return data

    @post_dump
    def make_response(self, data, **kwargs):
        return data

    def get_str_date(self, dt):
        return dt.format('YYYY-MM-DDTHH:mm:ss.SSSZZ')