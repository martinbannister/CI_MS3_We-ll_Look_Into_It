function flash_toast(msg, category) {
    // use category for styling
    let styling = 'rounded';
    switch(category) {
        case 'flash_error':
            styling += ' orange darken-4';
            break;
        case 'flash_success':
            styling += ' lime accent-4 grey-text text-darken-4';
            break;
        default:

    }
    M.toast({html: msg, classes: styling });
  }