import json
import flask
from methods import internal_methods

@internal_methods.verifyFacilityID
@internal_methods.verifyDockerEngine(swarm_method=True)
def swarmGetNodeInfo(facility_id, app_name="", app_id="") -> flask.Response:
  """
  Returns information on specified node

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
    app_name (optional) - this value is passed as an http parameter

  returns:
    if successful, returns node information in json format
  """

  # get list of node names
  completedProcess = internal_methods.subprocessRun("docker node ls --format {{.Hostname}}")
  if completedProcess.returncode != 0:
      return flask.make_response(f"Unknown error:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)
  name_list = completedProcess.stdout.decode().strip().split("\n")

  # check that node exists
  hostname = flask.request.args.get("hostname")
  if hostname == None:
    return flask.make_response(f"No hostname provided", 400)
  if hostname not in name_list:
    return flask.make_response(f"Unable to find node '{hostname}'", 400)

  # inspect specified node
  completedProcess = internal_methods.subprocessRun(f"docker node inspect --format json {hostname}")
  if completedProcess.returncode != 0:
    return flask.make_response(f"Unknown error:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

  return flask.make_response(json.dumps(json.loads(completedProcess.stdout.decode())), 200)