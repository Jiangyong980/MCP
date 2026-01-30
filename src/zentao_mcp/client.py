"""Zentao API Client"""
import requests
from typing import Optional, Dict, Any, List
import logging

from .config import ZentaoConfig

logger = logging.getLogger(__name__)


class ZentaoClient:
    """Client for Zentao API"""
    
    def __init__(self, config: Optional[ZentaoConfig] = None):
        self.config = config or ZentaoConfig.from_env()
        self.session = requests.Session()
        self._token: Optional[str] = None
        self.base_path = f"{self.config.base_url.rstrip('/')}/api.php/v1"
        
    def _ensure_authenticated(self):
        """Ensure we have a valid token"""
        if not self._token:
            self._authenticate()
    
    def _authenticate(self):
        """Authenticate and get token"""
        url = f"{self.config.base_url.rstrip('/')}/api.php/v1/tokens"
        payload = {
            "account": self.config.username,
            "password": self.config.password
        }
        
        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            self._token = data.get("token")
            logger.info("Successfully authenticated with Zentao")
        except requests.RequestException as e:
            logger.error(f"Authentication failed: {e}")
            raise
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with token"""
        self._ensure_authenticated()
        return {"Token": self._token} if self._token else {}
    
    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict] = None,
        json_data: Optional[Dict] = None
    ) -> Any:
        """Make a request to Zentao API"""
        url = f"{self.base_path}{path}"
        headers = self._get_headers()
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json_data
            )
            response.raise_for_status()
            return response.json() if response.text else None
        except requests.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise
    
    # ==================== Programs ====================
    
    def list_programs(self, order: Optional[str] = None) -> Dict:
        """Get list of programs"""
        params = {}
        if order:
            params["order"] = order
        return self._request("GET", "/programs", params=params)
    
    def get_program(self, program_id: int) -> Dict:
        """Get program details"""
        return self._request("GET", f"/programs/{program_id}")
    
    def create_program(self, data: Dict) -> Dict:
        """Create a new program"""
        return self._request("POST", "/programs", json_data=data)
    
    def update_program(self, program_id: int, data: Dict) -> Dict:
        """Update a program"""
        return self._request("PUT", f"/programs/{program_id}", json_data=data)
    
    def delete_program(self, program_id: int) -> Dict:
        """Delete a program"""
        return self._request("DELETE", f"/programs/{program_id}")
    
    # ==================== Products ====================
    
    def list_products(self) -> Dict:
        """Get list of products"""
        return self._request("GET", "/products")
    
    def get_product(self, product_id: int) -> Dict:
        """Get product details"""
        return self._request("GET", f"/products/{product_id}")
    
    def create_product(self, data: Dict) -> Dict:
        """Create a new product"""
        return self._request("POST", "/products", json_data=data)
    
    def update_product(self, product_id: int, data: Dict) -> Dict:
        """Update a product"""
        return self._request("PUT", f"/products/{product_id}", json_data=data)
    
    def delete_product(self, product_id: int) -> Dict:
        """Delete a product"""
        return self._request("DELETE", f"/products/{product_id}")
    
    def get_product_stories(self, product_id: int) -> Dict:
        """Get stories for a product"""
        return self._request("GET", f"/products/{product_id}/stories")
    
    def get_product_bugs(self, product_id: int) -> Dict:
        """Get bugs for a product"""
        return self._request("GET", f"/products/{product_id}/bugs")
    
    # ==================== Projects ====================
    
    def list_projects(self, page: int = 1, limit: int = 20) -> Dict:
        """Get list of projects"""
        params = {"page": page, "limit": limit}
        return self._request("GET", "/projects", params=params)
    
    def get_project(self, project_id: int) -> Dict:
        """Get project details"""
        return self._request("GET", f"/projects/{project_id}")
    
    def create_project(self, data: Dict) -> Dict:
        """Create a new project"""
        return self._request("POST", "/projects", json_data=data)
    
    def update_project(self, project_id: int, data: Dict) -> Dict:
        """Update a project"""
        return self._request("PUT", f"/projects/{project_id}", json_data=data)
    
    def delete_project(self, project_id: int) -> Dict:
        """Delete a project"""
        return self._request("DELETE", f"/projects/{project_id}")
    
    def get_project_executions(self, project_id: int) -> Dict:
        """Get executions for a project"""
        return self._request("GET", f"/projects/{project_id}/executions")
    
    def get_project_stories(self, project_id: int) -> Dict:
        """Get stories for a project"""
        return self._request("GET", f"/projects/{project_id}/stories")
    
    # ==================== Executions ====================
    
    def list_executions(self) -> Dict:
        """Get list of executions"""
        return self._request("GET", "/executions")
    
    def get_execution(self, execution_id: int) -> Dict:
        """Get execution details"""
        return self._request("GET", f"/executions/{execution_id}")
    
    def create_execution(self, project_id: int, data: Dict) -> Dict:
        """Create a new execution in a project"""
        return self._request("POST", f"/projects/{project_id}/executions", json_data=data)
    
    def update_execution(self, execution_id: int, data: Dict) -> Dict:
        """Update an execution"""
        return self._request("PUT", f"/executions/{execution_id}", json_data=data)
    
    def delete_execution(self, execution_id: int) -> Dict:
        """Delete an execution"""
        return self._request("DELETE", f"/executions/{execution_id}")
    
    def get_execution_stories(self, execution_id: int) -> Dict:
        """Get stories for an execution"""
        return self._request("GET", f"/executions/{execution_id}/stories")
    
    def get_execution_tasks(self, execution_id: int) -> Dict:
        """Get tasks for an execution"""
        return self._request("GET", f"/executions/{execution_id}/tasks")
    
    # ==================== Stories ====================
    
    def get_story(self, story_id: int) -> Dict:
        """Get story details"""
        return self._request("GET", f"/stories/{story_id}")
    
    def create_story(self, data: Dict) -> Dict:
        """Create a new story"""
        return self._request("POST", "/stories", json_data=data)
    
    def update_story(self, story_id: int, data: Dict) -> Dict:
        """Update a story"""
        return self._request("PUT", f"/stories/{story_id}", json_data=data)
    
    def delete_story(self, story_id: int) -> Dict:
        """Delete a story"""
        return self._request("DELETE", f"/stories/{story_id}")
    
    def change_story(self, story_id: int, data: Dict) -> Dict:
        """Change a story (create new version)"""
        return self._request("POST", f"/stories/{story_id}/change", json_data=data)
    
    # ==================== Tasks ====================
    
    def get_task(self, task_id: int) -> Dict:
        """Get task details"""
        return self._request("GET", f"/tasks/{task_id}")
    
    def create_task(self, execution_id: int, data: Dict) -> Dict:
        """Create a new task in an execution"""
        return self._request("POST", f"/executions/{execution_id}/tasks", json_data=data)
    
    def update_task(self, task_id: int, data: Dict) -> Dict:
        """Update a task"""
        return self._request("PUT", f"/tasks/{task_id}", json_data=data)
    
    def delete_task(self, task_id: int) -> Dict:
        """Delete a task"""
        return self._request("DELETE", f"/tasks/{task_id}")
    
    # ==================== Bugs ====================
    
    def get_bug(self, bug_id: int) -> Dict:
        """Get bug details"""
        return self._request("GET", f"/bugs/{bug_id}")
    
    def create_bug(self, data: Dict) -> Dict:
        """Create a new bug"""
        return self._request("POST", "/bugs", json_data=data)
    
    def update_bug(self, bug_id: int, data: Dict) -> Dict:
        """Update a bug"""
        return self._request("PUT", f"/bugs/{bug_id}", json_data=data)
    
    def delete_bug(self, bug_id: int) -> Dict:
        """Delete a bug"""
        return self._request("DELETE", f"/bugs/{bug_id}")
    
    # ==================== Users ====================
    
    def list_users(self) -> Dict:
        """Get list of users"""
        return self._request("GET", "/users")
    
    def get_user(self, user_id: int) -> Dict:
        """Get user details"""
        return self._request("GET", f"/users/{user_id}")
    
    def get_my_info(self) -> Dict:
        """Get current user info"""
        return self._request("GET", "/user")
