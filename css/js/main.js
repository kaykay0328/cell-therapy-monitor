// 加载数据
async function loadData() {
    try {
        // 加载数据文件
        const response = await fetch('data/latest.json');
        const data = await response.json();
        
        // 更新统计数字
        document.getElementById('academic-count').textContent = data.counts.academic;
        document.getElementById('clinical-count').textContent = data.counts.clinical;
        document.getElementById('policy-count').textContent = data.counts.policy;
        
        // 更新最后更新时间
        document.getElementById('last-updated').textContent = data.lastUpdated;
        document.getElementById('next-update').textContent = data.nextUpdate;
        
        // 加载最新内容
        const latestContentElement = document.getElementById('latest-content');
        latestContentElement.innerHTML = ''; // 清空加载中消息
        
        // 添加最新学术研究
        const academicSection = document.createElement('div');
        academicSection.innerHTML = `
            <h3>最新学术研究</h3>
            <ul class="latest-list">
                ${data.latest.academic.map(item => `
                    <li>
                        <a href="${item.link}" target="_blank">${item.title}</a>
                        <span class="item-date">${item.date}</span>
                    </li>
                `).join('')}
            </ul>
        `;
        latestContentElement.appendChild(academicSection);
        
        // 添加最新临床进展
        const clinicalSection = document.createElement('div');
        clinicalSection.innerHTML = `
            <h3>最新临床进展</h3>
            <ul class="latest-list">
                ${data.latest.clinical.map(item => `
                    <li>
                        <a href="${item.link}" target="_blank">${item.title}</a>
                        <span class="item-date">${item.date}</span>
                    </li>
                `).join('')}
            </ul>
        `;
        latestContentElement.appendChild(clinicalSection);
        
        // 添加最新政策监控
        const policySection = document.createElement('div');
        policySection.innerHTML = `
            <h3>最新政策监控</h3>
            <ul class="latest-list">
                ${data.latest.policy.map(item => `
                    <li>
                        <a href="${item.link}" target="_blank">${item.title}</a>
                        <span class="item-date">${item.date}</span>
                    </li>
                `).join('')}
            </ul>
        `;
        latestContentElement.appendChild(policySection);
        
    } catch (error) {
        console.error('加载数据失败:', error);
        document.getElementById('latest-content').innerHTML = '<p>加载数据失败，请稍后再试。</p>';
    }
}

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', loadData);
