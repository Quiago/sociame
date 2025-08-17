import React from 'react';

const InstagramPost = ({ post, visual, index }) => {
  const hashtags = Array.isArray(post.hashtags) ? post.hashtags : [];
  
  // Determine image content
  const renderImageContent = () => {
    if (visual && visual.image_url) {
      return <img src={visual.image_url} alt="Generated content image" />;
    } else if (visual && visual.description) {
      return (
        <div className="placeholder-image">
          📸 Image not available
          <div style={{ marginTop: '10px', fontSize: '12px' }}>
            Use this description to create your image
          </div>
        </div>
      );
    } else {
      return (
        <div className="loading-image">
          🎨 Generating image...
          <div style={{ marginTop: '10px', fontSize: '12px' }}>
            Creating custom image for this post
          </div>
        </div>
      );
    }
  };

  return (
    <div className="instagram-post-card">
      <div className="instagram-post">
        <div className="instagram-header">
          <div className="instagram-profile">
            <div className="profile-pic">✨</div>
            <div className="profile-info">
              <div className="username">@content_creator</div>
              <div className="location">Creating content 📍</div>
            </div>
          </div>
          <div className="instagram-menu">⋯</div>
        </div>
        
        <div className="instagram-image">
          {renderImageContent()}
        </div>
        
        <div className="instagram-actions">
          <div className="action-buttons">
            <span className="action-btn">❤️</span>
            <span className="action-btn">💬</span>
            <span className="action-btn">📤</span>
          </div>
          <div className="bookmark">🔖</div>
        </div>
        
        <div className="instagram-likes">
          <strong>1,234 likes</strong>
        </div>
        
        <div className="instagram-caption">
          <div className="caption-text">
            <strong>@content_creator</strong> {post.hook}
            <br /><br />
            {post.body}
            <br /><br />
            {post.cta}
            <br /><br />
            <span className="hashtags-text">
              {hashtags.join(' ')}
            </span>
          </div>
        </div>
        
        <div className="instagram-comments">
          <div className="comment">
            <strong>@fan_user</strong> Amazing content! 😍
          </div>
          <div className="comment">
            <strong>@active_follower</strong> Excellent post! 👏
          </div>
          <div className="view-comments">View all 47 comments</div>
        </div>
        
        <div className="instagram-time">
          2 hours ago
        </div>
      </div>
    </div>
  );
};

export default InstagramPost;