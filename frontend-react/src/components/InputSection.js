import React, { useState } from 'react';

const InputSection = ({ onGenerate, isGenerating }) => {
  const [currentTab, setCurrentTab] = useState('text');
  const [formData, setFormData] = useState({
    text: '',
    url: '',
    image: null,
    niche: '',
    objective: '',
    tone: ''
  });
  const [imagePreview, setImagePreview] = useState(null);

  const handleTabChange = (tab) => {
    setCurrentTab(tab);
    // Clear inputs when switching tabs
    setFormData({
      text: '',
      url: '',
      image: null,
      niche: '',
      objective: '',
      tone: ''
    });
    setImagePreview(null);
  };

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
      setFormData(prev => ({
        ...prev,
        image: file
      }));
      
      // Create preview
      const reader = new FileReader();
      reader.onload = (e) => {
        setImagePreview({
          url: e.target.result,
          name: file.name
        });
      };
      reader.readAsDataURL(file);
    }
  };

  const validateInput = () => {
    switch (currentTab) {
      case 'text':
        if (!formData.text.trim()) {
          return { isValid: false, message: 'Please enter a text or topic.' };
        }
        break;
      case 'url':
        if (!formData.url.trim()) {
          return { isValid: false, message: 'Please enter a URL.' };
        }
        try {
          new URL(formData.url);
        } catch {
          return { isValid: false, message: 'Please enter a valid URL.' };
        }
        break;
      case 'image':
        if (!formData.image) {
          return { isValid: false, message: 'Please select an image.' };
        }
        break;
      case 'guided':
        if (!formData.niche.trim() || !formData.objective || !formData.tone) {
          return { isValid: false, message: 'Please complete all guided form fields.' };
        }
        break;
      default:
        return { isValid: false, message: 'Select a valid input type.' };
    }
    return { isValid: true };
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (isGenerating) return;

    const validation = validateInput();
    if (!validation.isValid) {
      alert(validation.message);
      return;
    }

    const apiFormData = new FormData();
    apiFormData.append('input_type', currentTab);

    switch (currentTab) {
      case 'text':
        apiFormData.append('content', formData.text.trim());
        break;
      case 'url':
        apiFormData.append('content', formData.url.trim());
        break;
      case 'image':
        apiFormData.append('image', formData.image);
        break;
      case 'guided':
        const guidedAnswers = {
          niche: formData.niche.trim(),
          objective: formData.objective,
          tone: formData.tone
        };
        apiFormData.append('guided_answers', JSON.stringify(guidedAnswers));
        break;
    }

    onGenerate(apiFormData);
  };

  return (
    <section className="input-section">
      <h2>How do you want to generate content?</h2>
      
      <div className="input-tabs">
        <button 
          className={`tab-btn ${currentTab === 'text' ? 'active' : ''}`}
          onClick={() => handleTabChange('text')}
        >
          📝 Text
        </button>
        <button 
          className={`tab-btn ${currentTab === 'url' ? 'active' : ''}`}
          onClick={() => handleTabChange('url')}
        >
          🔗 URL
        </button>
        <button 
          className={`tab-btn ${currentTab === 'image' ? 'active' : ''}`}
          onClick={() => handleTabChange('image')}
        >
          🖼️ Image
        </button>
        <button 
          className={`tab-btn ${currentTab === 'guided' ? 'active' : ''}`}
          onClick={() => handleTabChange('guided')}
        >
          🎯 Guided
        </button>
      </div>

      <form onSubmit={handleSubmit}>
        {/* Text Input Tab */}
        {currentTab === 'text' && (
          <div className="tab-content active">
            <div className="input-group">
              <label htmlFor="text-input">Describe your topic or context:</label>
              <textarea 
                id="text-input"
                value={formData.text}
                onChange={(e) => handleInputChange('text', e.target.value)}
                placeholder="Example: 'Easy vegan recipes for beginners that can be made in 15 minutes'"
                rows="4"
              />
            </div>
          </div>
        )}

        {/* URL Input Tab */}
        {currentTab === 'url' && (
          <div className="tab-content active">
            <div className="input-group">
              <label htmlFor="url-input">Instagram profile or website URL:</label>
              <input 
                type="url"
                id="url-input"
                value={formData.url}
                onChange={(e) => handleInputChange('url', e.target.value)}
                placeholder="https://instagram.com/example_profile"
              />
              <small>We'll analyze the style and content to create similar posts</small>
            </div>
          </div>
        )}

        {/* Image Input Tab */}
        {currentTab === 'image' && (
          <div className="tab-content active">
            <div className="input-group">
              <label htmlFor="image-input">Upload an image to analyze:</label>
              <div className="file-upload">
                <input 
                  type="file"
                  id="image-input"
                  accept="image/*"
                  onChange={handleImageChange}
                />
                <div className="file-upload-text">
                  <span>📸 Drag an image here or click to select</span>
                </div>
              </div>
              {imagePreview && (
                <div className="image-preview">
                  <img src={imagePreview.url} alt="Preview" />
                  <p>Selected image: {imagePreview.name}</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Guided Input Tab */}
        {currentTab === 'guided' && (
          <div className="tab-content active">
            <div className="input-group">
              <label htmlFor="niche-input">What niche or industry is your account about?</label>
              <input 
                type="text"
                id="niche-input"
                value={formData.niche}
                onChange={(e) => handleInputChange('niche', e.target.value)}
                placeholder="Ex: vegan cooking, fitness, technology..."
              />
            </div>
            
            <div className="input-group">
              <label htmlFor="objective-select">What's the goal of your next post?</label>
              <select 
                id="objective-select"
                value={formData.objective}
                onChange={(e) => handleInputChange('objective', e.target.value)}
              >
                <option value="">Select a goal</option>
                <option value="entertain">Entertain</option>
                <option value="educate">Educate</option>
                <option value="sell">Sell</option>
                <option value="inspire">Inspire</option>
                <option value="inform">Inform</option>
              </select>
            </div>
            
            <div className="input-group">
              <label htmlFor="tone-select">What tone of voice do you prefer?</label>
              <select 
                id="tone-select"
                value={formData.tone}
                onChange={(e) => handleInputChange('tone', e.target.value)}
              >
                <option value="">Select a tone</option>
                <option value="fun">Fun</option>
                <option value="professional">Professional</option>
                <option value="inspiring">Inspiring</option>
                <option value="casual">Casual</option>
                <option value="educational">Educational</option>
              </select>
            </div>
          </div>
        )}

        <button 
          type="submit" 
          className="generate-btn"
          disabled={isGenerating}
        >
          {isGenerating ? 'Generating...' : '✨ Generate Content'}
        </button>
      </form>
    </section>
  );
};

export default InputSection;