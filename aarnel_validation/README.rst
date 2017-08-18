======================================================================
Aarnel validation: cálculo de proximidad fonética de dos strings.
======================================================================

-------------------------------
Invocación
-------------------------------
Para efecutar un test y llamar la función desde un servidor autenticado, usar:

.. code-block :: python

  import json
  import boto3

  data = {
    "address_1": u'XXXXX XXXXX XXXXX XXXXX XXXXX',
    "address_2": u'XXXXX XXXXX XXXXX XXXXX XXXXX',
    "percent_strength": xx,
    "word": "AV|AVENIDA|BLOQUE|BLOCK|PJ|PJE|ENTREGAR|PASAJE|PA|"
    "CASA|DP|DPTO|DEPARTAMENTO|EDIF",
    "special": "!|@|#|$|/|.|-|\\u00b0"
  }

  client = boto3.client(
    'lambda',
    region_name='us-east-1'
  )

  response = client.invoke(
    FunctionName="arn:aws:lambda:us-east-1:242956272159:function:aarnel_validation",
    Payload=json.dumps(data)
  )
  print("Response: {}".format(json.loads(response['Payload'].read())))


La respuesta obtenida será un diccionario con la información complementaria del perfil buscado.

.. code-block :: python

  {u'True'}
  {u'False'}
