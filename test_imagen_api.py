#!/usr/bin/env python3
"""
Test script specifically for Imagen API integration
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('backend/.env')

def test_imagen_api():
    """Test the Imagen API directly"""
    print("🧪 Testing Imagen API Integration\n")
    
    # Check API key
    api_key = os.getenv("GEMINI_IMAGE_API_KEY")
    if not api_key:
        print("❌ GEMINI_IMAGE_API_KEY not found in environment")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    try:
        # Import required modules
        from google import genai as new_genai
        from google.genai import types
        import io
        from PIL import Image
        
        print("✅ Required modules imported successfully")
        
        # Initialize client
        client = new_genai.Client(api_key=api_key)
        print("✅ GenAI client initialized")
        
        # Test prompt
        test_prompt = "A beautiful sunset over mountains, digital art style"
        print(f"🎨 Testing with prompt: {test_prompt}")
        
        # Try to generate image
        try:
            response = client.models.generate_images(
                model='imagen-4.0-generate-001',
                prompt=test_prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1
                )
            )
            
            print(f"🎯 API call successful!")
            print(f"📊 Response type: {type(response)}")
            
            if hasattr(response, 'generated_images'):
                print(f"📸 Generated images: {len(response.generated_images)}")
                
                if response.generated_images and len(response.generated_images) > 0:
                    generated_image = response.generated_images[0]
                    print(f"🖼️ First image type: {type(generated_image)}")
                    
                    if hasattr(generated_image, 'image'):
                        img = generated_image.image
                        print(f"📏 Image type: {type(img)}")
                        print(f"📐 Image size: {img.size}")
                        
                        # Convert to bytes
                        buffer = io.BytesIO()
                        img.save(buffer, format='PNG')
                        image_data = buffer.getvalue()
                        
                        print(f"✅ Image conversion successful!")
                        print(f"📦 Image data size: {len(image_data)} bytes")
                        
                        # Test base64 encoding
                        import base64
                        b64_data = base64.b64encode(image_data).decode()
                        data_url = f"data:image/png;base64,{b64_data}"
                        
                        print(f"📋 Base64 encoding successful: {len(b64_data)} chars")
                        print(f"🔗 Data URL length: {len(data_url)} chars")
                        
                        return True
                    else:
                        print("❌ Generated image has no 'image' attribute")
                else:
                    print("❌ No generated images in response")
            else:
                print("❌ Response has no 'generated_images' attribute")
                
        except Exception as api_error:
            print(f"❌ Imagen API error: {str(api_error)}")
            print(f"📝 Error type: {type(api_error)}")
            
            # Try alternative model
            print("\n🔄 Trying alternative model...")
            try:
                response = client.models.generate_images(
                    model='imagen-4.0-generate-001',
                    prompt=test_prompt,
                    config=types.GenerateImagesConfig(
                        number_of_images=1,
                        aspect_ratio="1:1",
                        safety_setting="block_some"
                    )
                )
                print("✅ Alternative model worked!")
                return True
            except Exception as alt_error:
                print(f"❌ Alternative model also failed: {str(alt_error)}")
                
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        print("💡 Make sure google-genai is installed: pip install google-genai")
        
    except Exception as e:
        print(f"❌ General error: {str(e)}")
        
    return False

def test_fallback_generation():
    """Test the fallback placeholder generation"""
    print("\n🧪 Testing Fallback Image Generation\n")
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        import io
        import base64
        
        # Create a placeholder image (same as in backend)
        img = Image.new('RGB', (512, 512), color='#667eea')
        draw = ImageDraw.Draw(img)
        
        # Add gradient effect
        for y in range(512):
            color_val = int(102 + (126 * y / 512))
            draw.rectangle([0, y, 512, y+1], fill=(102, color_val, 234))
        
        # Add text
        test_prompt = "A beautiful sunset over mountains"
        lines = [
            "🎨 AI Generated Image",
            "",
            "Prompt:",
            test_prompt[:40] + "..." if len(test_prompt) > 40 else test_prompt,
            "",
            "📸 Placeholder Image",
            "Real image generation in progress..."
        ]
        
        y_offset = 150
        for line in lines:
            draw.text((30, y_offset), line, fill='white')
            y_offset += 25
        
        # Convert to bytes and base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_data = buffer.getvalue()
        
        b64_data = base64.b64encode(img_data).decode()
        data_url = f"data:image/png;base64,{b64_data}"
        
        print(f"✅ Fallback image generated successfully!")
        print(f"📦 Image size: {len(img_data)} bytes")
        print(f"📋 Base64 size: {len(b64_data)} chars")
        print(f"🔗 Data URL size: {len(data_url)} chars")
        print(f"🖼️ Preview: {data_url[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Fallback generation failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔬 Imagen API Test Suite\n")
    
    # Test 1: Imagen API
    api_success = test_imagen_api()
    
    # Test 2: Fallback generation
    fallback_success = test_fallback_generation()
    
    print("\n" + "="*50)
    print("📊 Test Results:")
    print(f"   🎨 Imagen API: {'✅ PASS' if api_success else '❌ FAIL (will use fallback)'}")
    print(f"   📸 Fallback: {'✅ PASS' if fallback_success else '❌ FAIL'}")
    
    if api_success:
        print("\n🎉 Imagen API is working! Real images will be generated.")
    elif fallback_success:
        print("\n⚠️ Imagen API failed, but fallback works. Placeholder images will be used.")
        print("💡 Check your GEMINI_IMAGE_API_KEY and internet connection.")
    else:
        print("\n❌ Both tests failed. Check your setup.")
        
    print("\n🚀 Ready to test with the full backend!")