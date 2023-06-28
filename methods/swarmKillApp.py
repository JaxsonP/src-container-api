import subprocess
import flask
from . import internal_methods


@internal_methods.verifyFacilityID
@internal_methods.verifyDockerEngine
@internal_methods.handleSwarmAppName
def swarmKillApp(facility_id, app_name="", app_id="") -> flask.Response:
  """
  Sends a command to docker to kill and remove the specified app

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
    app_name - this value is passed as an http parameter
  """

  # executing system command
  completedProcess = internal_methods.subprocessRun(f"docker service rm {app_id}", shell=True, capture_output=True)
  if completedProcess.returncode != 0:
    return flask.make_response("Failed to kill app:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

  return flask.make_response("Success", 200)