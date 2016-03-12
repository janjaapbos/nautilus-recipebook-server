# external imports
from nautilus import APIGateway

# local imports
from schema import schema

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
