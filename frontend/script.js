const postsGrid = document.getElementById('posts-grid');
const searchInput = document.getElementById('search-input');
const sentimentFilter = document.getElementById('sentiment-filter');
const refreshBtn = document.getElementById('refresh-btn');
const statusIndicator = document.getElementById('status-indicator');

// Modal Elements
const modal = document.getElementById("wordcloud-modal");
const btn = document.getElementById("wordcloud-btn");
const span = document.getElementsByClassName("close")[0];

let allPosts = [];

// Fetch posts from backend
async function fetchPosts() {
  try {
    statusIndicator.style.background = "orange"; // loading
    const res = await fetch("http://127.0.0.1:8000/api/posts");
    const data = await res.json();
    allPosts = data.posts || [];
    renderPosts(allPosts);
    statusIndicator.style.background = "#50E3C2"; // success
  } catch (err) {
    console.error(err);
    statusIndicator.style.background = "#F44336"; // error
  }
}

// Render posts with filter + search
function renderPosts(posts) {
  const filterValue = sentimentFilter.value;
  const searchValue = searchInput.value.toLowerCase();
  const filtered = posts.filter(post => {
    const sentimentMatch = filterValue === 'All' ? true : post.sentiment === filterValue;
    const searchMatch = post.title.toLowerCase().includes(searchValue);
    return sentimentMatch && searchMatch;
  });

  postsGrid.innerHTML = filtered.map(post => `
    <div class="post-card">
      <a href="${post.link}" target="_blank">${post.title}</a>
      <div class="published">${new Date(post.published).toLocaleString()}</div>
      <div class="badge ${post.sentiment}">${post.sentiment}</div>
    </div>
  `).join('') || '<p>No posts found.</p>';
}

// Event Listeners
searchInput.addEventListener('input', () => renderPosts(allPosts));
sentimentFilter.addEventListener('change', () => renderPosts(allPosts));
refreshBtn.addEventListener('click', fetchPosts);

// Auto-refresh every 10s
setInterval(fetchPosts, 10000);

// Modal Events
btn.onclick = async () => {
  modal.style.display = "flex";
  try {
    const res = await fetch("http://127.0.0.1:8000/api/posts");
    const data = await res.json();
    generateWordCloud(data.posts);
    generateTrendChart(data.posts);
  } catch (err) {
    console.error(err);
  }
};
span.onclick = () => { modal.style.display = "none"; };
window.onclick = (e) => { if(e.target === modal) modal.style.display = "none"; };

// WordCloud
function generateWordCloud(posts) {
  const text = posts.map(p => p.cleaned).join(' ');
  const words = text.split(/\s+/).filter(w => w.length > 3);
  const freqMap = {};
  words.forEach(word => freqMap[word] = (freqMap[word] || 0) + 1);
  const wordArray = Object.entries(freqMap);

  WordCloud(document.getElementById('wordcloud-canvas'), {
    list: wordArray,
    gridSize: 16,
    weightFactor: 8,
    fontFamily: 'Inter, sans-serif',
    color: () => '#4A90E2',
    rotateRatio: 0.3,
    backgroundColor: '#fff'
  });
}

// Trend Chart
function generateTrendChart(posts) {
  const hours = [...Array(24).keys()];
  const positiveCounts = Array(24).fill(0);
  const negativeCounts = Array(24).fill(0);

  posts.forEach(post => {
    const hour = new Date(post.published).getHours();
    if(post.sentiment === 'POSITIVE') positiveCounts[hour]++;
    if(post.sentiment === 'NEGATIVE') negativeCounts[hour]++;
  });

  const ctx = document.getElementById('trend-chart').getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: hours.map(h => `${h}:00`),
      datasets: [
        { label: 'Positive', data: positiveCounts, borderColor: '#50E3C2', fill: false, tension: 0.3 },
        { label: 'Negative', data: negativeCounts, borderColor: '#F44336', fill: false, tension: 0.3 }
      ]
    },
    options: { responsive: true, plugins: { legend: { position: 'top' } } }
  });
}

// Initial fetch
fetchPosts();
