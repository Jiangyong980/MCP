"""Test script for Zentao MCP Client"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from zentao_mcp.client import ZentaoClient
from zentao_mcp.config import ZentaoConfig


def test_client():
    """Test Zentao client with real API"""
    # Load config from env
    config = ZentaoConfig.from_env()
    
    if not config.is_valid():
        print("❌ Configuration incomplete!")
        print("Please set environment variables:")
        print("  - ZENTAO_BASE_URL")
        print("  - ZENTAO_USERNAME")
        print("  - ZENTAO_PASSWORD")
        return
    
    print(f"🔗 Connecting to: {config.base_url}")
    print(f"👤 Username: {config.username}")
    
    client = ZentaoClient(config)
    
    try:
        # Test 1: Get current user info
        print("\n📋 Test 1: Get my info")
        my_info = client.get_my_info()
        print(f"✅ Success: {my_info}")
        
        # Test 2: List products
        print("\n📋 Test 2: List products")
        products = client.list_products()
        print(f"✅ Found {products.get('total', 0)} products")
        if products.get('products'):
            print(f"   First product: {products['products'][0]['name']}")
        
        # Test 3: List projects
        print("\n📋 Test 3: List projects")
        projects = client.list_projects()
        print(f"✅ Found {projects.get('total', 0)} projects")
        
        # Test 4: List programs
        print("\n📋 Test 4: List programs")
        programs = client.list_programs()
        print(f"✅ Found {len(programs.get('programs', []))} programs")
        
        print("\n🎉 All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_client()
