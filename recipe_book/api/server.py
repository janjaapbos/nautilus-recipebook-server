# external imports
from nautilus import APIGateway as APIGatewayBase

# local imports
from schema import schema


class APIGateway(APIGatewayBase):

    def setup_jwt(self):
        self.app.add_url_rule('/get_jwt', 'get_jwt', self.get_jwt, methods=['GET', 'POST'])
        self.app.before_request(self.process_jwt)

    def get_jwt(self):
        import jwt
        from flask import request, make_response, g
        import json

        token_value, response = self.gen_jwt_value(request, make_response)
        if response:
            return response

        token = jwt.encode(
            token_value,
            self.app.config.get('JWT_KEY', 'changeme'),
            algorithm='HS256'
        )
        id_token = json.dumps(dict(id_token=token.decode('ascii')))
        response = make_response(id_token)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        #response.set_cookie('jwt', token, domain='.example.com')
        return response

    def gen_jwt_value(self, request, make_response):
        from datetime import datetime, timedelta
        response = None
        username = request.args.get('user', "Test user")
        jwt_value = dict(
            username=username,
            role="Test role",
            exp=datetime.utcnow() + timedelta(minutes=self.app.config.get('HAPYAK_JWT_LIFETIME', 60)),
            iat=datetime.utcnow()
        )
        return jwt_value, response

    def process_jwt(self):
        from flask import request, make_response, g
        import jwt

        token = request.headers.get(
                'Authorization',
        )
        if not token or token.lower() in ["bearer null", "bearer undefined"]:
            return
        token = token[7:]
        try:
            user_info = jwt.decode(
                token,
                self.app.config.get('JWT_KEY', 'changeme'),
                algorithms=['HS256']
            )
            g.user_info = user_info
        except jwt.ExpiredSignatureError as e:
            response = make_response('Your JWT has expired')
            response.status_code = 401
            return response
        except jwt.DecodeError as e:
            response = make_response('Your JWT is invalid')
            response.status_code = 401
            return response
# create a nautilus service with just the schema
service = APIGateway(schema=schema)

import json
open('schema.json', 'w').write(
     json.dumps(
         {'data': schema.introspect()},
         indent=2,
         sort_keys=True
     )
)

service.setup_jwt()
