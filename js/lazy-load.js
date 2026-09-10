// 真正的视频懒加载脚本
// 配合 data-src 和 data-lazy 使用

document.addEventListener('DOMContentLoaded', function() {
    console.log('🎬 懒加载脚本已启动');
    
    // 查找所有需要懒加载的视频
    const lazyVideos = document.querySelectorAll('video[data-lazy="true"]');
    console.log(`📹 找到 ${lazyVideos.length} 个待懒加载视频`);
    
    if (lazyVideos.length === 0) {
        console.log('ℹ️  没有需要懒加载的视频');
        return;
    }
    
    // 创建 Intersection Observer
    const videoObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const video = entry.target;
                const source = video.querySelector('source[data-src]');
                
                if (source && source.dataset.src) {
                    console.log(`✅ 加载视频: ${source.dataset.src}`);
                    
                    // 设置 src
                    source.src = source.dataset.src;
                    
                    // 移除 data-src 避免重复加载
                    delete source.dataset.src;
                    
                    // 加载视频
                    video.load();
                    
                    // 尝试自动播放
                    video.play().catch(e => {
                        console.log('⚠️  自动播放被阻止，可能需要用户交互:', e);
                    });
                    
                    // 移除 data-lazy 标记
                    video.removeAttribute('data-lazy');
                    
                    // 停止观察
                    observer.unobserve(video);
                }
            }
        });
    }, {
        rootMargin: '100px 0px',  // 提前100px开始加载
        threshold: 0.1
    });
    
    // 观察所有懒加载视频
    lazyVideos.forEach(video => {
        videoObserver.observe(video);
    });
    
    // 处理折叠内容的视频懒加载
    const toggleHeaders = document.querySelectorAll('.divHeader');
    toggleHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const content = this.nextElementSibling;
            if (content && content.classList.contains('divToggleContent')) {
                // 延迟检查，确保内容已展开
                setTimeout(() => {
                    const videos = content.querySelectorAll('video[data-lazy="true"]');
                    videos.forEach(video => {
                        const rect = video.getBoundingClientRect();
                        // 如果视频在视口内
                        if (rect.top < window.innerHeight && rect.bottom > 0) {
                            const source = video.querySelector('source[data-src]');
                            if (source && source.dataset.src) {
                                console.log(`✅ 折叠展开后加载视频: ${source.dataset.src}`);
                                source.src = source.dataset.src;
                                delete source.dataset.src;
                                video.load();
                                video.play().catch(e => {
                                    console.log('⚠️  自动播放被阻止:', e);
                                });
                                video.removeAttribute('data-lazy');
                            }
                        }
                    });
                }, 200);
            }
        });
    });
    
    // 图片懒加载 (使用浏览器原生 loading="lazy")
    const lazyImages = document.querySelectorAll('img[data-src]');
    if (lazyImages.length > 0) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    delete img.dataset.src;
                    observer.unobserve(img);
                }
            });
        }, {
            rootMargin: '50px 0px',
            threshold: 0.01
        });
        
        lazyImages.forEach(img => {
            imageObserver.observe(img);
        });
    }
    
    console.log('✅ 懒加载脚本初始化完成');
});

// 提供手动加载接口（调试用）
window.loadAllVideos = function() {
    const videos = document.querySelectorAll('video[data-lazy="true"]');
    videos.forEach(video => {
        const source = video.querySelector('source[data-src]');
        if (source && source.dataset.src) {
            source.src = source.dataset.src;
            delete source.dataset.src;
            video.load();
            video.play().catch(e => console.log('播放失败:', e));
            video.removeAttribute('data-lazy');
        }
    });
    console.log(`✅ 手动加载了 ${videos.length} 个视频`);
};

// 检查加载状态（调试用）
window.checkVideoStatus = function() {
    const allVideos = document.querySelectorAll('video');
    let loaded = 0;
    let pending = 0;
    
    allVideos.forEach(video => {
        if (video.dataset.lazy === 'true') {
            pending++;
        } else {
            loaded++;
        }
    });
    
    console.log(`📊 视频状态: 已加载 ${loaded}, 待加载 ${pending}`);
    return { loaded, pending };
};
