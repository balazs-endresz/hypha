(function ($) {

    'use strict';

    const $body = $('body');
    const $checkbox = $('.js-batch-select');
    const $allCheckboxInput = $('.js-batch-select-all');
    const activeClass = 'batch-actions-enabled';

    $allCheckboxInput.change(function() {
        if ($(this).is(':checked')) {
            $checkbox.each(function() {
                this.checked = true;
            });
        } else {
            $checkbox.each(function() {
                this.checked = false;
            });
        }

        updateCount();
    })

    $checkbox.change(function () {

        // see how many checkboxes are :checked
        checkTotalSelected();

        // updates selected checbox count
        updateCount();
    });

    function checkTotalSelected() {
        if ($('.js-batch-select:checked').length) {
            $body.addClass(activeClass);
        }
        else {
            $body.removeClass(activeClass);
        }
    }

    function updateCount() {
        $('.js-total-actions').html($('.js-batch-select:checked').length);
    }



})(jQuery);
