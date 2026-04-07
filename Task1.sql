-- Summary jadvalini yaratish va hisob-kitob qilish
CREATE TABLE IF NOT EXISTS book_summary AS
SELECT
    year AS publication_year,
    COUNT(*) AS book_count,
    ROUND(AVG(
        CASE
            -- € belgisini olib tashlab, 1.2 ga ko'paytirish (USD ga o'tkazish)
            WHEN price LIKE '€%' THEN REPLACE(REPLACE(price, '€', ''), ',', '')::NUMERIC * 1.2
            -- $ belgisini olib tashlash
            WHEN price LIKE '$%' THEN REPLACE(REPLACE(price, '$', ''), ',', '')::NUMERIC
            ELSE REPLACE(price, ',', '')::NUMERIC
        END
    ), 2) AS average_price_usd
FROM books
GROUP BY year
ORDER BY year DESC;