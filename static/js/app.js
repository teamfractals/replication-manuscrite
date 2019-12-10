$(document).ready(
    function(){
        $('#uploadBtn').attr('disabled',true);
        $('input:file').change(
            function(){
                if ($(this).val()){
                    $('#uploadBtn').removeAttr('disabled'); 
                }
                else {
                    $('#uploadBtn').attr('disabled',true);
                }
            }
        );
    }
);
$(document).foundation();
