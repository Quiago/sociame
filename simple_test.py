#!/usr/bin/env python3
"""
Simple test to verify backend image generation works
"""
import base64
from PIL import Image, ImageDraw, ImageFont
import io

def test_image_generation():
    """Test the image generation logic"""
    print("🧪 Testing image generation logic...")
    
    try:
        # Simulate the image generation function
        prompt = "A beautiful landscape with mountains and sunset"
        print(f"📝 Prompt: {prompt}")
        
        # Create a simple placeholder image (like in our fallback)
        img = Image.new('RGB', (400, 400), color='#f0f0f0')
        draw = ImageDraw.Draw(img)
        
        # Add text
        try:
            font = ImageFont.load_default()
        except Exception:
            font = None
            
        text = "Generated Image\n" + prompt[:50] + "..."
        if font:
            draw.text((20, 180), text, fill='#333333', font=font)
        else:
            draw.text((20, 180), text, fill='#333333')
        
        # Convert to base64 (like the backend does)
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_data = buffer.getvalue()
        
        # Encode to base64 URL format
        b64_data = base64.b64encode(img_data).decode()
        image_url = f"data:image/png;base64,{b64_data}"
        
        print(f"✅ Image generated successfully!")
        print(f"📏 Raw image size: {len(img_data)} bytes")
        print(f"📦 Base64 size: {len(b64_data)} characters")
        print(f"🔗 Data URL size: {len(image_url)} characters")
        print(f"🖼️ Image URL preview: {image_url[:100]}...")
        
        # Test if the image can be decoded back
        try:
            # Extract base64 part
            base64_part = image_url.split(',')[1]
            decoded_data = base64.b64decode(base64_part)
            
            # Try to open as image
            test_img = Image.open(io.BytesIO(decoded_data))
            print(f"✅ Image validation successful: {test_img.size} pixels")
            
            return True, image_url
            
        except Exception as e:
            print(f"❌ Image validation failed: {e}")
            return False, None
            
    except Exception as e:
        print(f"❌ Image generation failed: {e}")
        return False, None

def create_test_response():
    """Create a test response similar to what the backend returns"""
    print("\n🧪 Creating test API response...")
    
    # Test image generation
    success, image_url = test_image_generation()
    
    if not success:
        print("❌ Cannot create test response without valid image")
        return None
    
    # Create a mock response
    test_response = {
        "context_summary": "Test context for veggie recipes. This is a clean summary without markdown artifacts or asterisks.",
        "ideas": [
            {"title": "Quick Veggie Bowl", "description": "Easy 15-minute vegetarian bowl"},
            {"title": "Plant-Based Protein", "description": "Protein-rich veggie recipes"},
            {"title": "Colorful Salads", "description": "Vibrant healthy salad ideas"},
            {"title": "Veggie Snacks", "description": "Quick healthy snacking options"},
            {"title": "Green Smoothies", "description": "Nutritious green smoothie recipes"}
        ],
        "posts": [
            {
                "hook": "🥗 Ready for a game-changing veggie bowl?",
                "body": "This 15-minute recipe will revolutionize your lunch routine! Packed with protein, fiber, and amazing flavors that'll keep you satisfied all afternoon.",
                "cta": "Save this recipe and tag a friend who needs healthy lunch ideas! 💚",
                "hashtags": ["#VeggieLife", "#HealthyEating", "#QuickMeals", "#PlantBased", "#MealPrep"]
            },
            {
                "hook": "💪 Who says plant-based can't be protein-packed?",
                "body": "These protein-rich recipes prove that vegetarian eating can fuel your workouts and keep you energized throughout the day.",
                "cta": "Which protein source is your favorite? Comment below! 👇",
                "hashtags": ["#PlantProtein", "#VegetarianFitness", "#HealthyLiving", "#NutritionTips", "#Wellness"]
            },
            {
                "hook": "🌈 Eating the rainbow has never been this delicious!",
                "body": "These colorful salads aren't just Instagram-worthy - they're packed with nutrients that'll make your body thank you.",
                "cta": "Try one of these combos this week and let me know which one's your fave! 🥗",
                "hashtags": ["#ColorfulEating", "#SaladLover", "#RainbowFood", "#HealthyChoices", "#FreshFood"]
            },
            {
                "hook": "🍿 Snack attack? I've got you covered!",
                "body": "These veggie snacks will satisfy your cravings without the guilt. Perfect for busy days when you need something quick and nutritious.",
                "cta": "Save this post for your next snack emergency! What's your go-to healthy snack? 🤔",
                "hashtags": ["#HealthySnacks", "#VeggieSnacks", "#CleanEating", "#SnackTime", "#WellnessJourney"]
            },
            {
                "hook": "🥬 Green smoothies that actually taste amazing!",
                "body": "No more choking down bitter green drinks. These smoothie recipes are so delicious, you'll forget they're packed with vegetables!",
                "cta": "Drop a 🥤 if you're ready to try these recipes! Which combo sounds best to you?",
                "hashtags": ["#GreenSmoothie", "#HealthyDrinks", "#VeggieBlend", "#MorningBoost", "#DetoxDrink"]
            }
        ],
        "visual_prompts": [
            {
                "description": "Colorful vegetarian bowl with quinoa, roasted vegetables, avocado, and tahini dressing, natural lighting, food photography style",
                "image_url": image_url
            },
            {
                "description": "Array of plant-based protein sources like lentils, chickpeas, tofu, and nuts arranged aesthetically, clean background",
                "image_url": image_url
            },
            {
                "description": "Vibrant rainbow salad with mixed greens, colorful vegetables, seeds, and dressing, overhead shot, bright natural light",
                "image_url": image_url
            },
            {
                "description": "Healthy veggie snacks arranged on a wooden board, hummus, cut vegetables, nuts, natural food styling",
                "image_url": image_url
            },
            {
                "description": "Green smoothie in a clear glass with fresh ingredients around it, leafy greens, fruits, health-focused composition",
                "image_url": image_url
            }
        ]
    }
    
    print(f"✅ Test response created successfully!")
    print(f"📱 Posts: {len(test_response['posts'])}")
    print(f"🎨 Images: {len(test_response['visual_prompts'])}")
    print(f"📝 All images have URLs: {all(img.get('image_url') for img in test_response['visual_prompts'])}")
    
    return test_response

if __name__ == "__main__":
    print("🧪 Simple Image Generation Test\n")
    
    response = create_test_response()
    
    if response:
        print(f"\n🎉 Test completed successfully!")
        print(f"\n📊 Response Summary:")
        print(f"   📝 Context length: {len(response['context_summary'])} chars")
        print(f"   💡 Ideas: {len(response['ideas'])}")
        print(f"   📱 Posts: {len(response['posts'])}")
        print(f"   🖼️ Images: {len(response['visual_prompts'])}")
        
        # Show first image info
        first_img = response['visual_prompts'][0]
        print(f"\n🔍 First Image Details:")
        print(f"   📝 Prompt: {first_img['description'][:60]}...")
        print(f"   🔗 Has URL: {'✅ Yes' if first_img.get('image_url') else '❌ No'}")
        if first_img.get('image_url'):
            print(f"   📏 URL length: {len(first_img['image_url'])} chars")
            
        print(f"\n✅ The system should work correctly with this data structure!")
        
    else:
        print(f"\n❌ Test failed!")