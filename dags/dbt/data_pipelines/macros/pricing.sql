{% macro discounted_amount(extended_price, discount_percentage, scale=2) %}
    ({{ extended_price }} * (1 - cast({{ discount_percentage }} as decimal(16, {{ scale }}))))
{% endmacro %}
