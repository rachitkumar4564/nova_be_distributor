from marshmallow import Schema, fields, validate
from marshmallow_enum import EnumField
from app.utils import StatusEnum, IDEnum


class DistributorSchema(Schema):
    id = fields.UUID()
    phone_number = fields.Str(validate=validate.Length(min=10))
    first_name = fields.Str(validate=validate.Length(min=2))
    last_name = fields.Str(validate=validate.Length(min=2))
    id_type = EnumField(IDEnum)
    id_number = fields.Str(validate=validate.Length(min=5))
    status = EnumField(StatusEnum)
    otp = fields.Str(validate=validate.Length(min=6, max=6))
    created = fields.DateTime()
    modified = fields.DateTime()

    class Meta:
        fields = [
            "id",
            "phone_number",
            "first_name",
            "last_name",
            "id_type",
            "id_number",
            "status",
            "otp",
            "created",
            "modified",
        ]


class DistributorCreateSchema(Schema):
    phone_number = fields.Str(required=True, validate=validate.Length(min=10))
    first_name = fields.Str(required=True, validate=validate.Length(min=2))
    last_name = fields.Str(required=True, validate=validate.Length(min=2))
    id_type = EnumField(IDEnum, required=True)
    id_number = fields.Str(required=True, validate=validate.Length(min=5))

    class Meta:
        fields = [
            "phone_number",
            "first_name",
            "last_name",
            "id_type",
            "id_number",
        ]


class DistributorUpdateSchema(Schema):
    phone_number = fields.Str(validate=validate.Length(min=10))
    first_name = fields.Str(validate=validate.Length(min=2))
    last_name = fields.Str(validate=validate.Length(min=2))
    id_type = EnumField(IDEnum)
    id_number = fields.Str(validate=validate.Length(min=5))
    status = EnumField(StatusEnum)

    class Meta:
        fields = [
            "id",
            "phone_number",
            "first_name",
            "last_name",
            "id_type",
            "id_number",
            "status",
        ]
