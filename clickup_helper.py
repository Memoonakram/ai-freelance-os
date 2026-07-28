import requests


class ClickUpManager:
    def __init__(self, api_key, list_id):
        self.api_key = api_key
        self.list_id = list_id
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }

    def create_lead_task(self, client_name, proposal_text, budget, subtasks=None):
        url = f"https://api.clickup.com/api/v2/list/{self.list_id}/task"

        # Exact status matching ClickUp Space settings: 'to do'
        payload = {
            "name": f"Client Proposal - {client_name}",
            "description": f"Target Budget: {budget}\n\n--- PROPOSAL ---\n{proposal_text}",
            "status": "to do"
        }

        response = requests.post(url, json=payload, headers=self.headers)

        if response.status_code in [200, 201]:
            task_data = response.json()
            task_id = task_data.get("id")

            # Subtasks Creation
            if subtasks and task_id:
                for sub in subtasks:
                    sub_payload = {
                        "name": sub,
                        "parent": task_id
                    }
                    requests.post(url, json=sub_payload, headers=self.headers)

            return task_data
        else:
            raise Exception(f"ClickUp Error [{response.status_code}]: {response.text}")