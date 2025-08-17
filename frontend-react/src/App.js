import React, { useState } from 'react';
import InputSection from './components/InputSection';
import LoadingSection from './components/LoadingSection';
import ResultsSection from './components/ResultsSection';
import ErrorSection from './components/ErrorSection';
import './index.css';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [currentView, setCurrentView] = useState('input'); // 'input', 'loading', 'results', 'error'
  const [results, setResults] = useState(null);
  const [error, setError] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerate = async (formData) => {
    setIsGenerating(true);
    setCurrentView('loading');
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/generate-content`, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Server error');
      }

      const data = await response.json();
      setResults(data);
      setCurrentView('results');
    } catch (err) {
      console.error('Error generating content:', err);
      setError(err.message || 'Unexpected error. Please try again.');
      setCurrentView('error');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleNewGeneration = () => {
    setCurrentView('input');
    setResults(null);
    setError('');
  };

  const handleRetry = () => {
    // This would require storing the last form data, for now just go back to input
    setCurrentView('input');
    setError('');
  };

  return (
    <div className="container">
      <header className="header">
        <h1>🚀 Community Manager Assistant</h1>
        <p className="subtitle">Generate Instagram content with AI</p>
      </header>

      <main className="main-content">
        {currentView === 'input' && (
          <InputSection 
            onGenerate={handleGenerate}
            isGenerating={isGenerating}
          />
        )}
        
        {currentView === 'loading' && <LoadingSection />}
        
        {currentView === 'results' && (
          <ResultsSection 
            results={results}
            onNewGeneration={handleNewGeneration}
          />
        )}
        
        {currentView === 'error' && (
          <ErrorSection 
            error={error}
            onRetry={handleRetry}
          />
        )}
      </main>
    </div>
  );
}

export default App;