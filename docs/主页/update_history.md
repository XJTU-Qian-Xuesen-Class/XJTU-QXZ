# Changelog

<!-- 动态提示框容器 -->
<div class="changelog-notice">
  <div class="notice-icon">ℹ️</div>
  <div class="notice-content">
    <p>本页的更新记录从 git commit log 自动生成，目前有以下特性：</p>
    <ul>
      <li>根据年份分组，有具体更改日期标注</li>
      <li>对应的 commit sha 值点击可以跳转到 GitHub 上对应的 commit 页面</li>
      <li>commit message 中带有课程名的部分点击可以跳转到网站上对应页面
        <ul>
          <li>该 commit 中有修改，但没有体现在 message 中的会将跳转链接列在二级列表中</li>
          <li>2025.7.20 之前的 commit 会跳转到存档站中对应页面</li>
        </ul>
      </li>
      <li>从 pull request 而来的 commit 可以通过末尾的 <code>#pr</code> 跳转到对应的 pull request 页面</li>
    </ul>
  </div>
</div>

<!-- 动态样式：适配 MkDocs Material 主题 -->
<style>
.changelog-notice {
  display: flex;
  align-items: flex-start;
  background: var(--md-default-bg-color);
  color: var(--md-default-fg-color);
  border: 2px solid var(--md-typeset-a-color);
  border-radius: 8px;
  padding: 16px;
  margin: 24px 0;
}

.notice-icon {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
  background: var(--md-typeset-a-color);
  color: var(--md-default-bg-color);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin-right: 12px;
  font-size: 14px;
}

.notice-content {
  line-height: 1.8;
}

.notice-content ul {
  margin: 0 0 0 20px;
  padding: 0;
  list-style: disc;
}

.notice-content ul ul {
  list-style: circle;
  margin-top: 4px;
}
</style>