import React, { useRef, useState } from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';
import { Navigation, Pagination } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';
import InstagramPost from './InstagramPost';

const PostsCarousel = ({ posts, visualPrompts }) => {
  const swiperRef = useRef(null);
  const [currentSlide, setCurrentSlide] = useState(0);
  const [isBeginning, setIsBeginning] = useState(true);
  const [isEnd, setIsEnd] = useState(false);
  const [copiedPrompt, setCopiedPrompt] = useState(false);

  if (!posts || posts.length === 0) {
    return (
      <div className="carousel-container">
        <div className="placeholder-image">
          No posts generated
        </div>
      </div>
    );
  }

  const handlePrev = () => {
    if (swiperRef.current && swiperRef.current.swiper) {
      swiperRef.current.swiper.slidePrev();
    }
  };

  const handleNext = () => {
    if (swiperRef.current && swiperRef.current.swiper) {
      swiperRef.current.swiper.slideNext();
    }
  };

  const handleSlideChange = (swiper) => {
    setCurrentSlide(swiper.activeIndex);
    setIsBeginning(swiper.isBeginning);
    setIsEnd(swiper.isEnd);
    setCopiedPrompt(false); // Reset copied state when slide changes
  };

  const copyToClipboard = async (text) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedPrompt(true);
      setTimeout(() => setCopiedPrompt(false), 2000);
    } catch (err) {
      console.error('Error al copiar:', err);
      // Fallback for older browsers
      const textArea = document.createElement('textarea');
      textArea.value = text;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);
      setCopiedPrompt(true);
      setTimeout(() => setCopiedPrompt(false), 2000);
    }
  };

  // Get current visual prompt
  const currentVisual = visualPrompts && visualPrompts[currentSlide];

  return (
    <>
      {/* Current Image Description Section */}
      {currentVisual && currentVisual.description && (
        <div className="current-image-prompt-section">
          <h4>🖼️ Image description for post {currentSlide + 1}</h4>
          <p className="image-prompt-text">{currentVisual.description}</p>
          <button 
            className={`copy-prompt-btn ${copiedPrompt ? 'copied' : ''}`}
            onClick={() => copyToClipboard(currentVisual.description)}
          >
            {copiedPrompt ? '✅ Copied!' : '📋 Copy description'}
          </button>
        </div>
      )}

      <div className="carousel-container">
        {/* Custom Navigation Buttons for Desktop */}
        {posts.length > 1 && (
          <>
            <button 
              className={`custom-nav-btn custom-nav-prev ${isBeginning ? 'disabled' : ''}`}
              onClick={handlePrev}
              disabled={isBeginning}
            >
              ‹
            </button>
            <button 
              className={`custom-nav-btn custom-nav-next ${isEnd ? 'disabled' : ''}`}
              onClick={handleNext}
              disabled={isEnd}
            >
              ›
            </button>
          </>
        )}

      <Swiper
        ref={swiperRef}
        modules={[Navigation, Pagination]}
        spaceBetween={0}
        slidesPerView={1}
        navigation={false} // Disable default navigation
        pagination={{
          clickable: true,
          dynamicBullets: true,
        }}
        loop={false} // Disable loop for better UX with custom buttons
        onSlideChange={handleSlideChange}
        className="posts-swiper"
        style={{
          '--swiper-pagination-color': '#667eea',
        }}
      >
        {posts.map((post, index) => (
          <SwiperSlide key={index}>
            <InstagramPost 
              post={post} 
              visual={visualPrompts[index]} 
              index={index}
            />
          </SwiperSlide>
        ))}
      </Swiper>

      {/* Slide Counter */}
      {posts.length > 1 && (
        <div className="slide-counter">
          {currentSlide + 1} / {posts.length}
        </div>
      )}
      </div>
    </>
  );
};

export default PostsCarousel;