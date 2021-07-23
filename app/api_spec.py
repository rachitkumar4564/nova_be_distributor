"""OpenAPI v3 Specification"""

# apispec via OpenAPI
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

# Create an APISpec
from app.schema import (
    DistributorSchema,
    DistributorCreateSchema,
    DistributorUpdateSchema,
    ConfirmTokenSchema,
    AddPinSchema,
    ResendTokenSchema,
    LoginSchema,
    TokenSchema,
)

spec = APISpec(
    title="Nova Distributor Service",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

# register schemas with spec
# example
spec.components.schema("Distributor", schema=DistributorSchema)
spec.components.schema("DistributorCreate", schema=DistributorCreateSchema)
spec.components.schema("DistributorUpdate", schema=DistributorUpdateSchema)
spec.components.schema("ConfirmToken", schema=ConfirmTokenSchema)
spec.components.schema("PinData", schema=AddPinSchema)
spec.components.schema("ResendTokenData", schema=ResendTokenSchema)
spec.components.schema("LoginData", schema=LoginSchema)
spec.components.schema("TokenData", schema=TokenSchema)

# add swagger tags that are used for endpoint annotation
tags = [
    {"name": "Authentication", "description": "For distributor authentication."},
    {"name": "Distributor", "description": "Distributor crud operation and others"},
]

for tag in tags:
    print(f"Adding tag: {tag['name']}")
    spec.tag(tag)
