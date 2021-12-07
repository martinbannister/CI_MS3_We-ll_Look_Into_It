document.addEventListener('DOMContentLoaded', function() {
    let sidenav = document.querySelectorAll('.sidenav');
    M.Sidenav.init(sidenav);
    let FABs = document.querySelectorAll('.fixed-action-btn');
    M.FloatingActionButton.init(FABs);
  });