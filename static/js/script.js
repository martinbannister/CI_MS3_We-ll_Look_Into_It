document.addEventListener('DOMContentLoaded', function() {
    // SIDENAV
    let sidenav = document.querySelectorAll('.sidenav');
    M.Sidenav.init(sidenav);

    // FLOATING ACTION BUTTONS
    let FABs = document.querySelectorAll('.fixed-action-btn');
    M.FloatingActionButton.init(FABs, {toolbarEnabled: true});

    // SELECT BOXES
    let selectElems = document.querySelectorAll('select');
    // IF used to prevent errors in browser console
    if (selectElems) {
      M.FormSelect.init(selectElems);
    }

    // ACCORDIANS/COLLAPSIBLES
    let accords = document.querySelectorAll('.collapsible');
    M.Collapsible.init(accords);

    // TOOLTIPS
    let tooltips = document.querySelectorAll('.tooltipped');
    M.Tooltip.init(tooltips);

    // MODALS
    let modals = document.querySelectorAll('.modal');
    M.Modal.init(modals);
  });

function checkRegisterForm(e) {
    let elems = e.target.elements;
    let pass1 = elems.password.value;
    let pass2 = elems.confirm_password.value;

    if (pass1 != pass2) {
      e.preventDefault();
      M.toast({html: 'Please ensure passwords match'});
      return false;
    } else {
      console.log('submitting form');
      return true;
    }
  }