
from flask import Flask, json, g, request, abort, session
from app.kudo.service import Service as Kudo
from app.kudo.schema import GithubRepoSchema
from flask_cors import CORS
from flask_oidc import OpenIDConnect
from os import environ, path
from functools import wraps
from jwt import decode, exceptions
from okta import UsersClient

import json
app = Flask(__name__)
app.config.update({
    'SECRET_KEY': '1xasjscsacasjkcajkx2',
    'OIDC_CLIENT_SECRETS': path.abspath('app/http/api/client_secrets.json'),
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_SCOPES': ['openid', 'profile', 'email'],
    'OIDC_CALLBACK_ROUTE': '/oidc/callback',
    'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post',
    'OIDC_ID_TOKEN_COOKIE_NAME': 'oidc_token'
})
oidc = OpenIDConnect(app)

okta_client = UsersClient("https://dev-885573.okta.com/oauth2/default", "007vGAgm7z3nnZqTnA7oRfbpIRv1_pthDZkjE9vUqm")
CORS(app)



def login_required(f):
   @wraps(f)
   def wrap(*args, **kwargs):
       authorization = request.headers.get("authorization", None)
       if not authorization:
           return json.dumps({'error': 'no authorization token provied'}), 403, {'Content-type': 'application/json'}
       try:
           token = authorization.split(' ')[1]
           isTokenValid = oidc.validate_token(token)
           print('validate_token: ' + str(isTokenValid))
           if isTokenValid != True:
               return json.dumps({'error': 'invalid authorization token'}), 403, {'Content-type': 'application/json'}
           else:
               resp = decode(token, None, verify=False, algorithms=['HS256'])
               g.user = resp['sub']


       except exceptions.DecodeError as identifier:
           return json.dumps({'error': 'invalid authorization token'}), 403, {'Content-type': 'application/json'}

       return f(*args, **kwargs)

   return wrap

@app.route("/helloWorld")
@login_required
def getHelloWorld():
 return json_response('hello')


@app.route("/kudos", methods=["GET"])
@login_required
def index():
 return json_response(Kudo(g.user).find_all_kudos())


@app.route("/kudos", methods=["POST"])
@login_required
def create():
   github_repo = GithubRepoSchema().load(json.loads(request.data))

   if github_repo.errors:
     return json_response({'error': github_repo.errors}, 422)

   kudo = Kudo(g.user).create_kudo_for(github_repo)
   return json_response(kudo)


@app.route("/kudo/<int:repo_id>", methods=["GET"])
@login_required
def show(repo_id):
 kudo = Kudo(g.user).find_kudo(repo_id)

 if kudo:
   return json_response(kudo)
 else:
   return json_response({'error': 'kudo not found'}, 404)


@app.route("/kudo/<int:repo_id>", methods=["PUT"])
@login_required
def update(repo_id):
   github_repo = GithubRepoSchema().load(json.loads(request.data))

   if github_repo.errors:
     return json_response({'error': github_repo.errors}, 422)

   kudo_service = Kudo(g.user)
   if kudo_service.update_kudo_with(repo_id, github_repo):
     return json_response(github_repo.data)
   else:
     return json_response({'error': 'kudo not found'}, 404)


@app.route("/kudo/<int:repo_id>", methods=["DELETE"])
@login_required
def delete(repo_id):
 kudo_service = Kudo(g.user)
 if kudo_service.delete_kudo_for(repo_id):
   return json_response({})
 else:
   return json_response({'error': 'kudo not found'}, 404)


def json_response(payload, status=200):
 return (json.dumps(payload), status, {'content-type': 'application/json'})
