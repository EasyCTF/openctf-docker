import json

class TestGeneral():
	def test_api_is_running(self, client):
		response = json.loads(client.get("/api").data)
		assert response["success"] == 1

	def test_requires_setup(self, client):
		response = json.loads(client.get("/api/user/status").data)
		assert "redirect" in response and response["redirect"] == "/setup"