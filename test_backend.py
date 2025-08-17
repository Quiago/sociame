#!/usr/bin/env python3
"""
Script de prueba para verificar que el backend funciona correctamente
"""

import requests
import json
import base64

def test_backend():
    """Test the backend API endpoints"""
    base_url = "http://localhost:8000"
    
    # Test 1: Health check
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test 2: Generate content with text input
    print("\n🔍 Testing content generation...")
    try:
        data = {
            'input_type': 'text',
            'content': 'Recetas veganas fáciles para principiantes'
        }
        
        response = requests.post(f"{base_url}/api/generate-content", data=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Content generation successful!")
            print(f"📝 Context: {result['context_summary'][:100]}...")
            print(f"💡 Ideas generated: {len(result.get('ideas', []))}")
            print(f"📱 Posts generated: {len(result.get('posts', []))}")
            print(f"🎨 Visual prompts: {len(result.get('visual_prompts', []))}")
            
            # Check if images were generated
            if result.get('visual_prompts'):
                for i, visual in enumerate(result['visual_prompts']):
                    if visual.get('image_url'):
                        print(f"🖼️ Image {i+1}: Generated successfully")
                        # Check if it's a valid base64 image
                        if visual['image_url'].startswith('data:image/'):
                            print(f"   📏 Image data length: {len(visual['image_url'])} chars")
                        else:
                            print(f"   ⚠️ Invalid image format")
                    else:
                        print(f"📸 Image {i+1}: No image generated")
                        print(f"   📝 Prompt: {visual.get('description', 'No description')[:50]}...")
                        
            return True
        else:
            print(f"❌ Content generation failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Content generation failed: {e}")
        return False

def test_image_function():
    """Test image generation function directly"""
    print("\n🔍 Testing image generation function...")
    
    try:
        import sys
        import os
        
        # Add backend directory to path
        backend_path = os.path.join(os.path.dirname(__file__), 'backend')
        sys.path.insert(0, backend_path)
        
        from main import generate_image_with_imagen
        
        # Test image generation
        test_prompt = "A beautiful sunset over mountains, digital art style"
        print(f"🎨 Testing with prompt: {test_prompt}")
        
        image_data = generate_image_with_imagen(test_prompt)
        
        if image_data:
            print(f"✅ Image generated successfully!")
            print(f"📏 Image data size: {len(image_data)} bytes")
            
            # Try to encode to base64
            try:
                import base64
                b64_data = base64.b64encode(image_data).decode()
                print(f"📦 Base64 encoding successful: {len(b64_data)} chars")
                return True
            except Exception as e:
                print(f"❌ Base64 encoding failed: {e}")
                return False
        else:
            print(f"❌ No image data returned")
            return False
            
    except Exception as e:
        print(f"❌ Image generation test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing CM Assistant Backend\n")
    
    # Test image function first
    image_test = test_image_function()
    
    print("\n" + "="*50)
    
    # Test full backend
    backend_test = test_backend()
    
    print("\n" + "="*50)
    print(f"📊 Test Results:")
    print(f"   🎨 Image Generation: {'✅ PASS' if image_test else '❌ FAIL'}")
    print(f"   🌐 Backend API: {'✅ PASS' if backend_test else '❌ FAIL'}")
    
    if image_test and backend_test:
        print(f"\n🎉 All tests passed! Backend is ready to use.")
    else:
        print(f"\n⚠️ Some tests failed. Check the logs above.")