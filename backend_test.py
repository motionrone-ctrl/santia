#!/usr/bin/env python3
import requests
import sys
import json
from datetime import datetime

class SantiaAPITester:
    def __init__(self, base_url="https://medhelp-cm.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name, success, details=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED")
        else:
            print(f"❌ {name} - FAILED: {details}")
        
        self.test_results.append({
            "test": name,
            "success": success,
            "details": details
        })

    def test_api_health(self):
        """Test basic API connectivity"""
        try:
            response = requests.get(f"{self.base_url}/api/", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}, Response: {response.text[:100]}"
            self.log_test("API Health Check", success, details)
            return success
        except Exception as e:
            self.log_test("API Health Check", False, str(e))
            return False

    def test_intake_endpoint_validation(self):
        """Test intake endpoint with invalid data"""
        try:
            # Test missing consent
            invalid_data = {
                "category": "sante-sexuelle",
                "symptoms": "Test symptoms",
                "duration": "1-4-semaines",
                "name": "Test User",
                "age": 25,
                "gender": "homme",
                "phone": "+237600000000",
                "email": "test@example.com",
                "city": "Douala",
                "consent": False  # Should fail
            }
            
            response = requests.post(
                f"{self.base_url}/api/intake", 
                json=invalid_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            success = response.status_code == 400
            details = f"Status: {response.status_code}, Expected 400 for missing consent"
            self.log_test("Intake Validation - Missing Consent", success, details)
            return success
        except Exception as e:
            self.log_test("Intake Validation - Missing Consent", False, str(e))
            return False

    def test_intake_creation(self):
        """Test successful intake creation"""
        try:
            valid_data = {
                "category": "sante-sexuelle",
                "symptoms": "Douleurs abdominales depuis 3 jours",
                "duration": "1-4-semaines",
                "history": "Aucun antécédent particulier",
                "name": "Jean Dupont",
                "age": 30,
                "gender": "homme",
                "phone": "+237600123456",
                "email": "jean.dupont@example.com",
                "city": "Douala",
                "consent": True
            }
            
            response = requests.post(
                f"{self.base_url}/api/intake", 
                json=valid_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                required_fields = ['id', 'category', 'symptoms', 'name', 'email', 'status', 'created_at']
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    success = False
                    details = f"Missing fields in response: {missing_fields}"
                else:
                    details = f"Intake created successfully with ID: {data.get('id', 'N/A')}"
                    self.intake_id = data.get('id')
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Intake Creation - Valid Data", success, details)
            return success
        except Exception as e:
            self.log_test("Intake Creation - Valid Data", False, str(e))
            return False

    def test_get_intakes(self):
        """Test retrieving intakes"""
        try:
            response = requests.get(f"{self.base_url}/api/intakes", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                if isinstance(data, list):
                    details = f"Retrieved {len(data)} intakes successfully"
                else:
                    success = False
                    details = "Response is not a list"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Get Intakes List", success, details)
            return success
        except Exception as e:
            self.log_test("Get Intakes List", False, str(e))
            return False

    def test_status_endpoints(self):
        """Test status check endpoints"""
        try:
            # Test status creation
            status_data = {"client_name": "test_client"}
            response = requests.post(
                f"{self.base_url}/api/status", 
                json=status_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            success = response.status_code == 200
            details = f"Status creation - Status: {response.status_code}"
            self.log_test("Status Creation", success, details)
            
            # Test status retrieval
            response = requests.get(f"{self.base_url}/api/status", timeout=10)
            success = response.status_code == 200
            details = f"Status retrieval - Status: {response.status_code}"
            self.log_test("Status Retrieval", success, details)
            
            return success
        except Exception as e:
            self.log_test("Status Endpoints", False, str(e))
            return False

    def run_all_tests(self):
        """Run all API tests"""
        print(f"🚀 Starting Santia API Tests - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌐 Testing API at: {self.base_url}")
        print("=" * 60)
        
        # Run tests in order
        if not self.test_api_health():
            print("❌ API is not accessible, stopping tests")
            return False
            
        self.test_intake_endpoint_validation()
        self.test_intake_creation()
        self.test_get_intakes()
        self.test_status_endpoints()
        
        # Print summary
        print("\n" + "=" * 60)
        print(f"📊 Test Summary: {self.tests_passed}/{self.tests_run} tests passed")
        success_rate = (self.tests_passed / self.tests_run) * 100 if self.tests_run > 0 else 0
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All tests passed!")
            return True
        else:
            print("⚠️  Some tests failed - check logs above")
            return False

def main():
    tester = SantiaAPITester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())