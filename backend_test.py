"""
Backend API Testing for FOMO Crypto Intelligence Terminal
=========================================================

Tests the key APIs mentioned in the review request:
- API /api/discovery/sources - 34 sources, 31 active, 3 needs_key
- API /api/news-intelligence/sources-registry - 120 news sources активны
- API /api/graph/stats - 281 nodes, 499 edges
- API /api/intel/stats - projects, investors, unlocks
- Discovery Health Check button - /api/discovery/sources/health-check
- News RSS parsing - Cointelegraph, The Block, Decrypt
- WebSocket - /api/ws/status returns channels
- Knowledge Graph search - a16z, Paradigm, Sequoia

Backend URL: https://frontend-backend-db-9.preview.emergentagent.com
"""

import requests
import sys
import json
from datetime import datetime
from typing import Dict, Any, List

# Use the public endpoint from frontend/.env
API_BASE_URL = "https://frontend-backend-db-9.preview.emergentagent.com"

class FOMOAPITester:
    def __init__(self, base_url=API_BASE_URL):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []
        
        # Test session with headers
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'FOMO-Testing/1.0'
        })

    def log_test_result(self, test_name: str, success: bool, details: Dict[str, Any]):
        """Log test result for reporting"""
        result = {
            'test_name': test_name,
            'success': success,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        self.tests_run += 1
        if success:
            self.tests_passed += 1

    def run_test(self, name: str, method: str, endpoint: str, expected_status: int = 200, 
                 data: Dict = None, params: Dict = None, timeout: int = 30) -> tuple:
        """Run a single API test"""
        url = f"{self.base_url}{endpoint}" if not endpoint.startswith('http') else endpoint
        
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {method} {url}")
        
        try:
            if method == 'GET':
                response = self.session.get(url, params=params, timeout=timeout)
            elif method == 'POST':
                response = self.session.post(url, json=data, params=params, timeout=timeout)
            elif method == 'PUT':
                response = self.session.put(url, json=data, params=params, timeout=timeout)
            else:
                raise ValueError(f"Unsupported method: {method}")

            success = response.status_code == expected_status
            
            # Try to parse JSON response
            try:
                json_data = response.json()
            except:
                json_data = {"raw_content": response.text[:500]}
            
            details = {
                'status_code': response.status_code,
                'expected_status': expected_status,
                'response_size': len(response.content),
                'response_time_ms': int(response.elapsed.total_seconds() * 1000),
                'response_data': json_data
            }
            
            if success:
                print(f"   ✅ PASSED - Status: {response.status_code}")
                if isinstance(json_data, dict):
                    # Log key metrics from response
                    if 'nodes' in json_data and 'edges' in json_data:
                        print(f"      📊 Graph: {json_data.get('nodes', 0)} nodes, {json_data.get('edges', 0)} edges")
                    elif 'sources' in json_data and isinstance(json_data['sources'], list):
                        print(f"      📋 Sources: {len(json_data['sources'])} items")
                    elif 'results' in json_data or 'items' in json_data:
                        items = json_data.get('results') or json_data.get('items', [])
                        if isinstance(items, list):
                            print(f"      📋 Items: {len(items)} results")
            else:
                print(f"   ❌ FAILED - Expected {expected_status}, got {response.status_code}")
                if response.text:
                    print(f"      Error: {response.text[:200]}...")
            
            self.log_test_result(name, success, details)
            return success, json_data

        except requests.exceptions.Timeout:
            print(f"   ⏰ TIMEOUT - Request timed out after {timeout}s")
            self.log_test_result(name, False, {'error': 'timeout', 'timeout_seconds': timeout})
            return False, {}
        except requests.exceptions.ConnectionError as e:
            print(f"   🔌 CONNECTION ERROR - {str(e)[:100]}")
            self.log_test_result(name, False, {'error': 'connection_error', 'message': str(e)[:200]})
            return False, {}
        except Exception as e:
            print(f"   💥 ERROR - {str(e)[:100]}")
            self.log_test_result(name, False, {'error': 'exception', 'message': str(e)[:200]})
            return False, {}

    def test_basic_health(self):
        """Test basic API health"""
        success, data = self.run_test(
            "Basic Health Check",
            "GET",
            "/api/health",
            200
        )
        return success

    def test_graph_stats(self):
        """Test /api/graph/stats - should return 281 nodes, 499 edges"""
        success, data = self.run_test(
            "Graph Statistics",
            "GET", 
            "/api/graph/stats",
            200
        )
        
        if success and isinstance(data, dict):
            nodes = data.get('nodes', 0)
            edges = data.get('edges', 0)
            
            # Check if we got the expected counts (approximately)
            expected_nodes = 281
            expected_edges = 499
            
            nodes_ok = abs(nodes - expected_nodes) < 50  # Allow some variance
            edges_ok = abs(edges - expected_edges) < 50
            
            if not nodes_ok:
                print(f"      ⚠️  Node count mismatch: expected ~{expected_nodes}, got {nodes}")
            if not edges_ok:
                print(f"      ⚠️  Edge count mismatch: expected ~{expected_edges}, got {edges}")
                
            return success and nodes_ok and edges_ok
        
        return success

    def test_discovery_sources(self):
        """Test /api/discovery/sources - should return 34 sources with proper status distribution"""
        success, data = self.run_test(
            "Discovery Sources (34 total, 31 active, 3 needs_key)",
            "GET",
            "/api/discovery/sources", 
            200
        )
        
        if success and isinstance(data, dict):
            sources = data.get('sources', [])
            total_count = len(sources)
            
            # Count sources by status
            status_counts = {}
            for source in sources:
                status = source.get('status', 'unknown')
                status_counts[status] = status_counts.get(status, 0) + 1
            
            print(f"      📊 Discovery Sources Summary:")
            print(f"         Total: {total_count}")
            for status, count in status_counts.items():
                print(f"         {status}: {count}")
            
            # Check if we have expected counts (with some tolerance)
            expected_total = 34
            expected_active_plus_degraded = 31  # Active sources
            expected_needs_key = 3
            
            actual_active = status_counts.get('active', 0) + status_counts.get('degraded', 0)
            actual_needs_key = status_counts.get('needs_key', 0)
            
            total_ok = abs(total_count - expected_total) <= 5
            active_ok = abs(actual_active - expected_active_plus_degraded) <= 5
            needs_key_ok = abs(actual_needs_key - expected_needs_key) <= 2
            
            if not total_ok:
                print(f"      ⚠️  Total source count: expected ~{expected_total}, got {total_count}")
            if not active_ok:
                print(f"      ⚠️  Active sources: expected ~{expected_active_plus_degraded}, got {actual_active}")
            if not needs_key_ok:
                print(f"      ⚠️  Sources needing keys: expected ~{expected_needs_key}, got {actual_needs_key}")
                
            return success and total_ok and (active_ok or needs_key_ok)
        
        return success

    def test_news_intelligence_sources_registry(self):
        """Test /api/news-intelligence/sources-registry - should return 120 active news sources"""
        success, data = self.run_test(
            "News Intelligence Sources Registry (120 sources)",
            "GET",
            "/api/news-intelligence/sources-registry",
            200
        )
        
        if success and isinstance(data, dict):
            sources = data.get('sources', [])
            stats = data.get('stats', {})
            
            total_sources = len(sources)
            active_count = stats.get('by_status', {}).get('active', 0)
            
            print(f"      📊 News Sources Registry:")
            print(f"         Total sources: {total_sources}")
            print(f"         Active sources: {active_count}")
            print(f"         By tier: {stats.get('by_tier', {})}")
            print(f"         By language: {stats.get('by_language', {})}")
            
            # Check if we have expected counts
            expected_total = 120
            total_ok = abs(total_sources - expected_total) <= 10
            active_ok = active_count >= 100  # Most should be active
            
            if not total_ok:
                print(f"      ⚠️  Total sources: expected ~{expected_total}, got {total_sources}")
            if not active_ok:
                print(f"      ⚠️  Active sources low: {active_count}")
            
            # Check key news sources (Cointelegraph, The Block, Decrypt)
            key_sources = ['cointelegraph', 'theblock', 'decrypt']
            found_sources = []
            for source in sources:
                if source.get('id') in key_sources:
                    found_sources.append(source.get('id'))
                    print(f"         ✅ {source.get('name')}: {source.get('status')} (health: {source.get('health_score')})")
            
            key_sources_ok = len(found_sources) >= 3
            if not key_sources_ok:
                print(f"      ⚠️  Missing key sources: {set(key_sources) - set(found_sources)}")
            
            return success and total_ok and active_ok and key_sources_ok
        
        return success

    def test_intel_stats(self):
        """Test /api/intel/stats - should return projects, investors, unlocks data"""
        success, data = self.run_test(
            "Intel Statistics",
            "GET",
            "/api/intel/stats",
            200
        )
        
        if success and isinstance(data, dict):
            collections = data.get('collections', {})
            
            print(f"      📊 Intel Collections:")
            for key, count in collections.items():
                print(f"         {key}: {count}")
            
            # Check for expected data
            investors = collections.get('investors', 0)
            projects = collections.get('projects', 0)
            unlocks = collections.get('unlocks', 0)
            
            # We should have some investors and projects seeded
            has_investors = investors >= 10
            has_projects = projects >= 20
            
            if not has_investors:
                print(f"      ⚠️  Low investors count: {investors}")
            if not has_projects:
                print(f"      ⚠️  Low projects count: {projects}")
                
            return success and has_investors and has_projects
        
        return success

    def test_discovery_health_check(self):
        """Test /api/discovery/sources/health-check - POST request to update statuses"""
        success, data = self.run_test(
            "Discovery Health Check", 
            "POST",
            "/api/discovery/sources/health-check",
            200
        )
        
        if success and isinstance(data, dict):
            # Check if health check response contains summary
            if 'summary' in data:
                summary = data['summary']
                print(f"      📊 Health Check Results:")
                print(f"         Total: {summary.get('total', 0)}")
                print(f"         Active: {summary.get('active', 0)}")
                print(f"         Degraded: {summary.get('degraded', 0)}")
                print(f"         Offline: {summary.get('offline', 0)}")
                return True
        
        return success

    def test_websocket_status(self):
        """Test /api/ws/status - should return WebSocket channels info"""
        success, data = self.run_test(
            "WebSocket Status",
            "GET",
            "/api/ws/status",
            200
        )
        
        if success and isinstance(data, dict):
            # Check for expected WebSocket response structure
            expected_fields = ['ok', 'total_connections', 'channels']
            has_expected = all(field in data for field in expected_fields)
            
            if has_expected:
                channels = data.get('channels', {})
                print(f"      📊 WebSocket Status:")
                print(f"         Total connections: {data.get('total_connections', 0)}")
                print(f"         Channels: {list(channels.keys())}")
                return True
            else:
                print(f"      ⚠️  Missing expected WebSocket fields: {expected_fields}")
                return False
        
        return success

    def test_knowledge_graph_search(self):
        """Test Knowledge Graph search for VC funds"""
        vc_funds = ['a16z', 'paradigm', 'jump crypto', 'sequoia']
        search_results = {}
        
        for fund in vc_funds:
            print(f"\n🔍 Searching Knowledge Graph for: {fund}")
            
            # Try graph search endpoint
            success, data = self.run_test(
                f"Knowledge Graph Search - {fund}",
                "GET",
                "/api/graph/search",
                200,
                params={'q': fund, 'limit': 10}
            )
            
            if success:
                results = data.get('results', []) or data.get('nodes', [])
                search_results[fund] = len(results) if isinstance(results, list) else 0
                print(f"      📋 Found {search_results[fund]} results for {fund}")
            else:
                # Try alternative search endpoint
                success2, data2 = self.run_test(
                    f"Alternative Search - {fund}",
                    "GET",
                    "/api/search",
                    200,
                    params={'q': fund, 'type': 'fund'}
                )
                if success2:
                    results = data2.get('results', [])
                    search_results[fund] = len(results) if isinstance(results, list) else 0
        
        # Check if we found results for major VC funds
        found_funds = sum(1 for count in search_results.values() if count > 0)
        print(f"\n📊 Knowledge Graph Search Summary:")
        for fund, count in search_results.items():
            print(f"   {fund}: {count} results")
        
        return found_funds >= 2  # At least 2 funds should have results

    def test_graph_visualization_data(self):
        """Test graph visualization endpoints"""
        # Test nodes endpoint
        nodes_success, nodes_data = self.run_test(
            "Graph Nodes",
            "GET",
            "/api/graph/nodes",
            200,
            params={'limit': 50}
        )
        
        # Test edges endpoint  
        edges_success, edges_data = self.run_test(
            "Graph Edges",
            "GET", 
            "/api/graph/edges",
            200,
            params={'limit': 50}
        )
        
        if nodes_success and edges_success:
            nodes = nodes_data.get('nodes', []) if isinstance(nodes_data, dict) else []
            edges = edges_data.get('edges', []) if isinstance(edges_data, dict) else []
            
            print(f"      📊 Graph Data: {len(nodes)} nodes, {len(edges)} edges retrieved")
            
            # Check if nodes have required fields for visualization
            if len(nodes) > 0:
                sample_node = nodes[0]
                node_fields = ['id', 'label', 'entity_type']
                has_node_fields = all(field in sample_node for field in node_fields)
                if not has_node_fields:
                    print(f"      ⚠️  Nodes missing visualization fields: {node_fields}")
                    return False
            
            # Check if edges have required fields
            if len(edges) > 0:
                sample_edge = edges[0]
                edge_fields = ['from_node_id', 'to_node_id', 'relation_type']
                has_edge_fields = all(field in sample_edge for field in edge_fields)
                if not has_edge_fields:
                    print(f"      ⚠️  Edges missing visualization fields: {edge_fields}")
                    return False
                    
            return True
        
        return False

    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting FOMO Crypto Intelligence Terminal API Tests")
        print(f"📡 Testing against: {self.base_url}")
        print("=" * 80)
        
        # Core API tests - Basic functionality
        self.test_basic_health()
        
        # Key APIs from review request
        self.test_discovery_sources()  # 34 sources, 31 active, 3 needs_key
        self.test_news_intelligence_sources_registry()  # 120 news sources
        self.test_graph_stats()  # 281 nodes, 499 edges
        self.test_intel_stats()  # projects, investors, unlocks
        
        # Health Check & Status
        self.test_discovery_health_check()
        self.test_websocket_status()
        
        # Knowledge Graph & Search
        self.test_knowledge_graph_search()
        
        # Optional visualization endpoints (may not be implemented)
        print(f"\n🔍 Testing optional graph visualization endpoints...")
        self.test_graph_visualization_data()
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        print(f"Total Tests: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%" if self.tests_run > 0 else "0%")
        
        # Detailed results for failed tests
        failed_tests = [t for t in self.test_results if not t['success']]
        if failed_tests:
            print(f"\n❌ FAILED TESTS ({len(failed_tests)}):")
            for test in failed_tests:
                print(f"   • {test['test_name']}")
                if 'error' in test['details']:
                    print(f"     Error: {test['details']['error']}")
                elif 'status_code' in test['details']:
                    print(f"     Status: {test['details']['status_code']} (expected {test['details']['expected_status']})")
        
        return self.tests_passed == self.tests_run


def main():
    """Main test execution"""
    tester = FOMOAPITester()
    success = tester.run_all_tests()
    
    # Save detailed results
    with open('/app/backend_test_results.json', 'w') as f:
        json.dump({
            'summary': {
                'total_tests': tester.tests_run,
                'passed_tests': tester.tests_passed,
                'failed_tests': tester.tests_run - tester.tests_passed,
                'success_rate': (tester.tests_passed/tester.tests_run*100) if tester.tests_run > 0 else 0,
                'test_timestamp': datetime.now().isoformat()
            },
            'test_results': tester.test_results
        }, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: /app/backend_test_results.json")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())