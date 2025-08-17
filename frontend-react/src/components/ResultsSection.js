import React from 'react';
import PostsCarousel from './PostsCarousel';

const ResultsSection = ({ results, onNewGeneration }) => {
  if (!results) return null;

  return (
    <section className="results-section">
      <h2>🎉 Your content is ready!</h2>
      
      {/* Post Idea Summary */}
      <div className="context-summary">
        <h3>📋 Post Idea</h3>
        <p>{results.context_summary}</p>
      </div>

      {/* Generated Posts Carousel with Image Description */}
      <div className="content-section">
        <h3>✍️ Generated Posts</h3>
        <PostsCarousel 
          posts={results.posts} 
          visualPrompts={results.visual_prompts}
        />
      </div>

      <button className="secondary-btn" onClick={onNewGeneration}>
        🔄 Generate new content
      </button>
    </section>
  );
};

export default ResultsSection;