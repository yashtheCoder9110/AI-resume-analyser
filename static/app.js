document.addEventListener('DOMContentLoaded', () => {
  const jobDescription = document.querySelector('#job_description');
  const characterCount = document.querySelector('[data-character-count]');
  const resumeInput = document.querySelector('#resumes');
  const filePreview = document.querySelector('[data-file-preview]');
  const matchForm = document.querySelector('[data-match-form]');
  const uploadDropzone = document.querySelector('[data-upload-dropzone]');
  const templateButtons = document.querySelectorAll('[data-template]');

  const updateCharacterCount = () => {
    if (jobDescription && characterCount) {
      characterCount.textContent = `${jobDescription.value.length.toLocaleString()} characters`;
    }
  };

  if (jobDescription) {
    jobDescription.addEventListener('input', updateCharacterCount);
    updateCharacterCount();
  }

  templateButtons.forEach((button) => {
    button.addEventListener('click', () => {
      if (!jobDescription) return;
      jobDescription.value = button.dataset.template || '';
      updateCharacterCount();
      templateButtons.forEach((item) => item.classList.toggle('active', item === button));
      jobDescription.focus();
    });
  });

  if (resumeInput && filePreview) {
    const updateResumeList = () => {
      const files = Array.from(resumeInput.files || []);
      filePreview.textContent = files.length
        ? `${files.length} resume${files.length === 1 ? '' : 's'} ready: ${files.map((file) => file.name).join(', ')}`
        : 'Choose one or more resumes to see them here.';
    };

    resumeInput.addEventListener('change', updateResumeList);
    updateResumeList();
  }

  if (uploadDropzone && resumeInput) {
    const preventDefault = (event) => {
      event.preventDefault();
      event.stopPropagation();
    };

    ['dragenter', 'dragover'].forEach((eventName) => {
      uploadDropzone.addEventListener(eventName, (event) => {
        preventDefault(event);
        uploadDropzone.classList.add('is-dragging');
      });
    });

    ['dragleave', 'drop'].forEach((eventName) => {
      uploadDropzone.addEventListener(eventName, (event) => {
        preventDefault(event);
        uploadDropzone.classList.remove('is-dragging');
      });
    });

    uploadDropzone.addEventListener('drop', (event) => {
      const files = event.dataTransfer?.files;
      if (!files || !files.length) return;
      resumeInput.files = files;
      resumeInput.dispatchEvent(new Event('change'));
    });
  }

  if (matchForm) {
    matchForm.addEventListener('submit', () => {
      const button = matchForm.querySelector('[data-submit-button]');
      const label = matchForm.querySelector('[data-submit-label]');
      const spinner = matchForm.querySelector('[data-submit-spinner]');
      if (button && label && spinner) {
        button.disabled = true;
        label.textContent = 'Analyzing resumes...';
        spinner.classList.remove('d-none');
      }
    });
  }

  const resultCards = Array.from(document.querySelectorAll('[data-candidate]'));
  const searchInput = document.querySelector('[data-result-search]');
  const sortSelect = document.querySelector('[data-result-sort]');
  const resultList = document.querySelector('[data-result-list]');
  const resultCount = document.querySelector('[data-result-count]');
  const emptyState = document.querySelector('[data-empty-filter]');
  const scoreFilters = Array.from(document.querySelectorAll('[data-score-filter]'));

  const updateResults = () => {
    if (!resultCards.length || !resultList || !searchInput || !sortSelect) return;

    const query = searchInput.value.trim().toLowerCase();
    const selectedFilter = document.querySelector('[data-score-filter].active')?.dataset.scoreFilter || 'all';
    const filteredCards = resultCards.filter((card) => {
      const matchesQuery = card.textContent.toLowerCase().includes(query);
      const matchesBand = selectedFilter === 'all' || card.dataset.scoreBand === selectedFilter;
      return matchesQuery && matchesBand;
    });

    const sortedCards = [...filteredCards].sort((first, second) => {
      if (sortSelect.value === 'name') return first.dataset.name.localeCompare(second.dataset.name);
      const scoreDifference = Number(second.dataset.score) - Number(first.dataset.score);
      return sortSelect.value === 'score-low' ? -scoreDifference : scoreDifference;
    });

    resultCards.forEach((card) => { card.classList.add('d-none'); });
    sortedCards.forEach((card) => {
      card.classList.remove('d-none');
      resultList.appendChild(card);
    });

    if (resultCount) resultCount.textContent = `Showing ${filteredCards.length} of ${resultCards.length} candidates`;
    if (emptyState) emptyState.classList.toggle('d-none', filteredCards.length > 0);
  };

  if (searchInput && sortSelect) {
    searchInput.addEventListener('input', updateResults);
    sortSelect.addEventListener('change', updateResults);
  }

  scoreFilters.forEach((filterButton) => {
    filterButton.addEventListener('click', () => {
      scoreFilters.forEach((button) => button.classList.toggle('active', button === filterButton));
      updateResults();
    });
  });

  if (resultCards.length) updateResults();
});