import pinject
from flask import Blueprint, request

from app.controllers import DistributorController
from app.definitions.service_result import handle_result
from app.repositories import DistributorRepository, LeadRepository
from app.schema import (
    DistributorCreateSchema,
    DistributorSchema,
    DistributorUpdateSchema,
    ConfirmTokenSchema,
    AddPinSchema,
    ResendTokenSchema,
    LoginSchema,
    TokenSchema,
)
from app.services import RedisService, AuthService
from app.utils import validator

distributor = Blueprint("distributor", __name__)

obj_graph = pinject.new_object_graph(
    modules=None,
    classes=[
        DistributorController,
        DistributorRepository,
        RedisService,
        AuthService,
        LeadRepository,
    ],
)
distributor_controller = obj_graph.provide(DistributorController)


@distributor.route("accounts/", methods=["POST"])
@validator(schema=DistributorCreateSchema)
def create_distributor():
    """
    ---
    post:
      description: creates a new distributor
      requestBody:
        required: true
        content:
          application/json:
            schema: DistributorCreate
      responses:
        '201':
          description: returns a distributor id
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: uuid
                    example: 3fa85f64-5717-4562-b3fc-2c963f66afa6
      tags:
          - Authentication
    """

    data = request.json
    result = distributor_controller.register(data)
    return handle_result(result, schema=DistributorSchema)


@distributor.route("/confirm-token", methods=["POST"])
@validator(schema=ConfirmTokenSchema)
def confirm_token():
    """
    ---
    post:
      description: creates a new distributor
      requestBody:
        required: true
        content:
            application/json:
                schema: ConfirmToken
      responses:
        '200':
          description: returns a distributor
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: string
                    example: m8bQ5_P8o_4eojNs4xUB6w
      tags:
          - Authentication
    """

    data = request.json
    result = distributor_controller.confirm_token(data)
    return handle_result(result)


@distributor.route("/resend-token", methods=["POST"])
@validator(schema=ResendTokenSchema)
def resend_token():
    """
    ---
    post:
      description: creates a new token
      requestBody:
        required: true
        content:
          application/json:
            schema: ResendTokenData
      responses:
        '200':
          description: resends a token
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: uuid
                    example: 3fa85f64-5717-4562-b3fc-2c963f66afa6
      tags:
          - Authentication
    """

    data = request.json
    result = distributor_controller.resend_token(data)
    return handle_result(result)


@distributor.route("/add-pin", methods=["POST"])
@validator(schema=AddPinSchema)
def add_pin():
    """
    ---
    post:
      description: creates a new distributor
      requestBody:
        required: true
        content:
            application/json:
                schema: PinData
      responses:
        '200':
          description: returns a distributor
          content:
            application/json:
              schema: TokenData
      tags:
          - Authentication
    """

    data = request.json
    result = distributor_controller.add_pin(data)
    return handle_result(result, schema=TokenSchema)


@distributor.route("/token_login", methods=["POST"])
@validator(schema=LoginSchema)
def login_user():
    """
    ---
    post:
      description: logs in a distributor
      requestBody:
        required: true
        content:
            application/json:
                schema: LoginSchema
      responses:
        '200':
          description: call successful
          content:
            application/json:
              schema: TokenData
      tags:
          - Authentication
    """

    data = request.json
    result = distributor_controller.login(data)
    return handle_result(result, schema=TokenSchema)


@distributor.route("/accounts/<string:customer_id>", methods=["PATCH"])
@validator(schema=DistributorUpdateSchema)
def update_distributor(distributor_id):
    """
    ---
    patch:
      description: updates a customer with id specified in path
      parameters:
        - in: path
          name: customer_id
          required: true
          schema:
            type: string
          description: The distributor ID
      requestBody:
        required: true
        content:
            application/json:
                schema: DistributorUpdate
      responses:
        '200':
          description: returns a customer
          content:
            application/json:
              schema: Distributor
      tags:
          - Distributor
    """

    data = request.json
    result = distributor_controller.update(distributor_id, data)
    return handle_result(result, schema=DistributorSchema)


@distributor.route("/accounts/<string:distributor_id>")
def show_distributor(distributor_id):
    """
    ---
    get:
      description: returns a distributor with id specified in path
      parameters:
        - in: path
          name: customer_id
          required: true
          schema:
            type: string
          description: The distributor ID
      responses:
        '200':
          description: returns a distributor
          content:
            application/json:
              schema: Customer
      tags:
          - Customer
    """
    result = distributor_controller.show(distributor_id)
    return handle_result(result, schema=DistributorSchema)


@distributor.route("/accounts/<string:distributor_id>", methods=["DELETE"])
def delete_distributor(distributor_id):
    """
    ---
    delete:
      description: deletes a distributor with id specified in path
      parameters:
        - in: path
          name: distributor_id
          required: true
          schema:
            type: string
          description: The distributor ID
      responses:
        '204':
          description: returns nil
      tags:
          - Distributor
    """
    result = distributor_controller.delete(distributor_id)
    return handle_result(result)
