#!/usr/bin/env python3
"""Test Google APIs and estimate spending"""
import os
import json
from datetime import datetime
from pathlib import Path
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent.parent / "local" / ".env")

class GoogleAPITester:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_MAPS_API_KEY not found in local/.env")
        
        # Track API calls and costs
        self.calls = []
        self.total_cost = 0.0
        
        # Pricing (as of 2024)
        self.pricing = {
            'static_maps': 0.002,  # $2 per 1000 requests after free tier
            'geocoding': 0.005,    # $5 per 1000 requests
            'places': 0.017,       # $17 per 1000 requests
        }
        
    def test_static_maps(self):
        """Test Static Maps API"""
        print("\n🗺️  Testing Static Maps API...")
        url = "https://maps.googleapis.com/maps/api/staticmap"
        params = {
            'center': 'Google HQ, Mountain View, CA',
            'zoom': 15,
            'size': '400x400',
            'key': self.api_key
        }
        
        response = requests.get(url, params=params)
        success = response.status_code == 200
        
        self.log_call('static_maps', success, response.status_code)
        
        if success:
            print(f"✓ Static Maps API working")
            print(f"  Response size: {len(response.content) / 1024:.1f} KB")
        else:
            print(f"✗ Static Maps API failed: {response.status_code}")
            
        return success
    
    def test_geocoding(self):
        """Test Geocoding API"""
        print("\n📍 Testing Geocoding API...")
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            'address': '1600 Amphitheatre Parkway, Mountain View, CA',
            'key': self.api_key
        }
        
        response = requests.get(url, params=params)
        success = response.status_code == 200
        
        self.log_call('geocoding', success, response.status_code)
        
        if success:
            data = response.json()
            if data.get('results'):
                location = data['results'][0]['geometry']['location']
                print(f"✓ Geocoding API working")
                print(f"  Location: {location['lat']}, {location['lng']}")
            else:
                print(f"✗ Geocoding API returned no results")
                success = False
        else:
            print(f"✗ Geocoding API failed: {response.status_code}")
            
        return success
    
    def test_places(self):
        """Test Places API (Find Place)"""
        print("\n🏢 Testing Places API...")
        url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        params = {
            'input': 'Golden Gate Bridge',
            'inputtype': 'textquery',
            'fields': 'name,geometry',
            'key': self.api_key
        }
        
        response = requests.get(url, params=params)
        success = response.status_code == 200
        
        self.log_call('places', success, response.status_code)
        
        if success:
            data = response.json()
            if data.get('candidates'):
                place = data['candidates'][0]
                print(f"✓ Places API working")
                print(f"  Found: {place.get('name', 'Unknown')}")
            else:
                print(f"✗ Places API returned no results")
                success = False
        else:
            print(f"✗ Places API failed: {response.status_code}")
            
        return success
    
    def check_quota(self):
        """Check API quota/usage (if available)"""
        print("\n📊 Checking API Usage...")
        # Note: Real-time quota checking requires Cloud Console API
        # This is a placeholder showing how you'd track it
        print(f"  Total API calls made: {len(self.calls)}")
        print(f"  Successful calls: {sum(1 for c in self.calls if c['success'])}")
        print(f"  Failed calls: {sum(1 for c in self.calls if not c['success'])}")
        
    def log_call(self, api_type, success, status_code):
        """Log an API call"""
        self.calls.append({
            'api': api_type,
            'success': success,
            'status_code': status_code,
            'timestamp': datetime.now().isoformat(),
            'cost': self.pricing.get(api_type, 0) if success else 0
        })
        if success:
            self.total_cost += self.pricing.get(api_type, 0)
    
    def estimate_costs(self):
        """Estimate costs based on usage"""
        print("\n💰 Cost Estimation:")
        print(f"  Free tier: $200/month credit")
        print(f"  Calls made in this session: {len(self.calls)}")
        print(f"  Estimated cost: ${self.total_cost:.4f}")
        
        # Monthly projection
        if self.calls:
            print("\n  📈 If you made this many calls daily:")
            daily_cost = self.total_cost
            print(f"     Daily: ${daily_cost:.4f}")
            print(f"     Monthly (30 days): ${daily_cost * 30:.2f}")
            print(f"     Yearly: ${daily_cost * 365:.2f}")
            
            # Free tier calculation
            monthly_projected = daily_cost * 30
            if monthly_projected <= 200:
                print(f"\n  ✓ Within free tier! ${200 - monthly_projected:.2f} remaining")
            else:
                print(f"\n  ⚠️  Would exceed free tier by ${monthly_projected - 200:.2f}")
    
    def save_usage_log(self):
        """Save usage log to file"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"google_api_usage_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'total_calls': len(self.calls),
            'total_cost': self.total_cost,
            'calls': self.calls
        }
        
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        print(f"\n📝 Usage log saved to: {log_file}")

def main():
    """Run all tests"""
    print("🧪 Google API Test Suite")
    print("=" * 50)
    
    try:
        tester = GoogleAPITester()
        
        # Run tests
        tests = [
            tester.test_static_maps,
            tester.test_geocoding,
            tester.test_places,
        ]
        
        results = []
        for test in tests:
            try:
                results.append(test())
            except Exception as e:
                print(f"✗ Error: {e}")
                results.append(False)
        
        # Summary
        print("\n" + "=" * 50)
        print("📋 Summary:")
        print(f"  Tests passed: {sum(results)}/{len(results)}")
        
        # Show usage and costs
        tester.check_quota()
        tester.estimate_costs()
        
        # Save log
        tester.save_usage_log()
        
        # Return success if all tests passed
        return all(results)
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
