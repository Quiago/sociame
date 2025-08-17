#!/usr/bin/env python3
"""
Full system test for the CM Assistant MVP
"""

import requests
import json
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('backend/.env')

def test_backend_health():
    """Test if backend is running"""
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend not accessible: {str(e)}")
        return False

def test_content_generation():
    """Test content generation with all input types"""
    print("\n🧪 Testing Content Generation\n")
    
    test_cases = [
        {
            "name": "Text Input",
            "data": {
                'input_type': 'text',
                'content': 'Consejos de marketing digital para pequeños negocios con presupuesto limitado'
            }
        },
        {
            "name": "URL Input", 
            "data": {
                'input_type': 'url',
                'content': 'https://example.com/marketing-tips'
            }
        },
        {
            "name": "Guided Input",
            "data": {
                'input_type': 'guided',
                'guided_answers': json.dumps({
                    "niche": "Marketing digital",
                    "objective": "educar",
                    "tone": "profesional"
                })
            }
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        print(f"🔍 Testing {test_case['name']}...")
        
        try:
            response = requests.post(
                "http://localhost:8000/api/generate-content",
                data=test_case['data'],
                timeout=60  # Give more time for image generation
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Analyze response
                context_length = len(data.get('context_summary', ''))
                num_ideas = len(data.get('ideas', []))
                num_posts = len(data.get('posts', []))
                num_visuals = len(data.get('visual_prompts', []))
                
                # Check if images were generated
                images_with_urls = sum(1 for visual in data.get('visual_prompts', []) 
                                     if visual.get('image_url'))
                
                print(f"   ✅ Success!")
                print(f"   📝 Context: {context_length} chars")
                print(f"   💡 Ideas: {num_ideas}")
                print(f"   📱 Posts: {num_posts}")
                print(f"   🎨 Visual prompts: {num_visuals}")
                print(f"   🖼️ Images generated: {images_with_urls}/{num_visuals}")
                
                # Check first post structure
                if data.get('posts'):
                    first_post = data['posts'][0]
                    required_fields = ['hook', 'body', 'cta', 'hashtags']
                    missing_fields = [field for field in required_fields 
                                    if not first_post.get(field)]
                    
                    if not missing_fields:
                        print(f"   📋 Post structure: ✅ Complete")
                    else:
                        print(f"   📋 Post structure: ❌ Missing {missing_fields}")
                
                # Check first visual prompt
                if data.get('visual_prompts'):
                    first_visual = data['visual_prompts'][0]
                    has_description = bool(first_visual.get('description'))
                    has_image = bool(first_visual.get('image_url'))
                    
                    print(f"   🎨 Visual structure: Description={has_description}, Image={has_image}")
                    
                    if has_image:
                        image_url = first_visual['image_url']
                        if image_url.startswith('data:image/'):
                            print(f"   🔗 Image format: ✅ Valid data URL ({len(image_url)} chars)")
                        else:
                            print(f"   🔗 Image format: ❌ Invalid format")
                
                results.append({
                    'test': test_case['name'],
                    'success': True,
                    'images': images_with_urls,
                    'total_visuals': num_visuals
                })
                
            else:
                print(f"   ❌ Failed with status {response.status_code}")
                print(f"   Error: {response.text}")
                results.append({
                    'test': test_case['name'],
                    'success': False,
                    'error': response.text
                })
                
        except requests.exceptions.Timeout:
            print(f"   ❌ Timeout (>60s)")
            results.append({
                'test': test_case['name'],
                'success': False,
                'error': 'Timeout'
            })
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            results.append({
                'test': test_case['name'],
                'success': False,
                'error': str(e)
            })
        
        print()  # Add spacing between tests
    
    return results

def test_api_keys():
    """Test if API keys are configured"""
    print("🔑 Checking API Keys...")
    
    text_key = os.getenv("GEMINI_TEXT_API_KEY")
    image_key = os.getenv("GEMINI_IMAGE_API_KEY")
    
    if text_key:
        print(f"   ✅ GEMINI_TEXT_API_KEY: {text_key[:10]}...")
    else:
        print(f"   ❌ GEMINI_TEXT_API_KEY: Not found")
    
    if image_key:
        print(f"   ✅ GEMINI_IMAGE_API_KEY: {image_key[:10]}...")
    else:
        print(f"   ❌ GEMINI_IMAGE_API_KEY: Not found")
    
    return bool(text_key and image_key)

def main():
    print("🚀 CM Assistant MVP - Full System Test\n")
    print("="*50)
    
    # Test 1: API Keys
    keys_ok = test_api_keys()
    print()
    
    # Test 2: Backend Health
    if not test_backend_health():
        print("\n❌ Backend not running. Please start with: cd backend && python main.py")
        return
    
    # Test 3: Content Generation
    if keys_ok:
        results = test_content_generation()
    else:
        print("⚠️ Skipping content generation tests due to missing API keys")
        results = []
    
    # Summary
    print("="*50)
    print("📊 Test Summary:")
    
    if results:
        successful_tests = sum(1 for r in results if r['success'])
        total_images = sum(r.get('images', 0) for r in results if r['success'])
        
        print(f"   🧪 Tests passed: {successful_tests}/{len(results)}")
        print(f"   🖼️ Images generated: {total_images}")
        
        if successful_tests == len(results):
            print(f"\n🎉 All tests passed! System is working correctly.")
            
            if total_images > 0:
                print(f"   ✅ Image generation is working")
            else:
                print(f"   ⚠️ Images using fallback placeholders")
                print(f"   💡 Check Imagen API configuration if you want real images")
                
        else:
            print(f"\n⚠️ Some tests failed. Check the logs above.")
    else:
        print(f"   ⚠️ No content generation tests performed")
    
    print(f"\n🌐 Frontend: Open http://localhost:3000 (React) to test the UI")
    print(f"🔧 Backend: Running on http://localhost:8000")

if __name__ == "__main__":
    main()