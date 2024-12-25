CREATE OR REPLACE FUNCTION archive_expired_data()
RETURNS VOID AS $$
BEGIN
    -- 将过期数据插入到 table_b
    INSERT INTO archived_data 
    SELECT *
    FROM disaster_data
    WHERE upload_date < NOW() - INTERVAL '1 year';

    -- 从 table_a 中删除已归档的数据
    DELETE FROM disaster_data
    WHERE upload_date < NOW() - INTERVAL '1 year';
END;
$$ LANGUAGE plpgsql;