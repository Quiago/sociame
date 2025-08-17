import React from 'react';

const ErrorSection = ({ error, onRetry }) => {
  return (
    <section className="error-section">
      <div className="error-message">
        <h3>❌ Oops! Something went wrong</h3>
        <p>{error}</p>
        <button className="secondary-btn" onClick={onRetry}>
          🔄 Try again
        </button>
      </div>
    </section>
  );
};

export default ErrorSection;