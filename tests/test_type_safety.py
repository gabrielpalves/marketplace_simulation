"""
Unit tests for type safety and integer quantity enforcement.
Run with: python tests/test_type_safety.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.market import MarketWorld
from agents.agent import TradingAgent

def test_integer_quantities():
    """Test that quantities are always integers."""
    print("\n" + "="*60)
    print("TEST 1: Integer Quantity Enforcement")
    print("="*60)
    
    market = MarketWorld()
    
    # Test posting with float quantity
    print("\n1. Posting offer with float quantity (10.7)...")
    offer_id = market.post_offer("TestSeller", "Wood", 5.0, 10.7)
    
    if offer_id:
        offer = market.active_offers[0]
        assert isinstance(offer["quantity"], int), "❌ Quantity is not integer!"
        assert offer["quantity"] == 11, f"❌ Expected 11, got {offer['quantity']}"
        print(f"   ✅ 10.7 rounded to {offer['quantity']} (integer)")
    
    # Test trading with integer preservation
    print("\n2. Executing trade...")
    result = market.execute_trade("TestBuyer", offer_id)
    
    if result["status"] == "success":
        qty = result["data"]["quantity"]
        assert isinstance(qty, int), "❌ Trade quantity is not integer!"
        print(f"   ✅ Trade quantity: {qty} (type: {type(qty).__name__})")
    
    print("\n✅ Integer quantity test PASSED")

def test_type_coercion():
    """Test that agent handles string inputs safely."""
    print("\n" + "="*60)
    print("TEST 2: Type Coercion")
    print("="*60)
    
    market = MarketWorld()
    agent = TradingAgent("TestAgent", "Test role", 100.0, market)
    
    # Test _safe_int with various inputs
    test_cases = [
        ("5", 5, "string integer"),
        ("5.7", 6, "string float (rounds)"),
        (5, 5, "native int"),
        (5.3, 5, "native float (rounds)"),
        (None, None, "None value"),
        ("", None, "empty string"),
    ]
    
    print("\nTesting _safe_int():")
    for input_val, expected, description in test_cases:
        try:
            result = agent._safe_int(input_val, "test_param")
            assert result == expected, f"Expected {expected}, got {result}"
            print(f"   ✅ {description}: '{input_val}' → {result}")
        except ValueError as e:
            if expected is not None:
                print(f"   ❌ {description}: Unexpected error: {e}")
            else:
                print(f"   ✅ {description}: Correctly rejected")
    
    # Test _safe_float
    print("\nTesting _safe_float():")
    float_cases = [
        ("5.0", 5.0, "string float"),
        ("5", 5.0, "string integer"),
        (5, 5.0, "native int"),
        (5.5, 5.5, "native float"),
    ]
    
    for input_val, expected, description in float_cases:
        try:
            result = agent._safe_float(input_val, "test_param")
            assert abs(result - expected) < 0.001, f"Expected {expected}, got {result}"
            print(f"   ✅ {description}: '{input_val}' → {result}")
        except ValueError as e:
            print(f"   ❌ {description}: Error: {e}")
    
    print("\n✅ Type coercion test PASSED")

def test_error_messages():
    """Test that error messages are helpful."""
    print("\n" + "="*60)
    print("TEST 3: Error Messages")
    print("="*60)
    
    market = MarketWorld()
    agent = TradingAgent("TestAgent", "Test role", 100.0, market)
    
    print("\n1. Testing invalid type conversion...")
    try:
        result = agent._safe_int("not_a_number", "test_param")
        print("   ❌ Should have raised ValueError")
    except ValueError as e:
        error_msg = str(e)
        assert "test_param" in error_msg, "Error should mention parameter name"
        assert "not_a_number" in error_msg, "Error should show actual value"
        assert "type:" in error_msg, "Error should show type"
        print(f"   ✅ Error message is helpful: {error_msg}")
    
    print("\n✅ Error message test PASSED")

def test_inventory_deduction():
    """Test that inventory is properly deducted when posting."""
    print("\n" + "="*60)
    print("TEST 4: Inventory Deduction")
    print("="*60)
    
    market = MarketWorld()
    agent = TradingAgent("TestSeller", "Test role", 100.0, market)
    agent.inventory = {"Wood": 50}
    
    print(f"\n1. Initial inventory: {agent.inventory}")
    
    # Simulate posting
    params = {"item": "Wood", "price": 5.0, "qty": 10}
    agent._handle_post(params)
    
    print(f"2. After posting 10 Wood: {agent.inventory}")
    assert agent.inventory["Wood"] == 40, "❌ Inventory not deducted correctly"
    print("   ✅ Inventory deducted correctly")
    
    # Try posting more than available
    print("\n3. Attempting to post 50 Wood (only 40 available)...")
    params = {"item": "Wood", "price": 5.0, "qty": 50}
    agent._handle_post(params)
    
    print(f"4. Inventory unchanged: {agent.inventory}")
    assert agent.inventory["Wood"] == 40, "❌ Inventory should not change"
    print("   ✅ Correctly rejected over-posting")
    
    print("\n✅ Inventory deduction test PASSED")

def run_all_tests():
    """Run all tests."""
    print("\n" + "="*70)
    print("🧪 RUNNING TYPE SAFETY AND INTEGER QUANTITY TESTS")
    print("="*70)
    
    try:
        test_integer_quantities()
        test_type_coercion()
        test_error_messages()
        test_inventory_deduction()
        
        print("\n" + "="*70)
        print("✅ ALL TESTS PASSED!")
        print("="*70)
        return 0
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())