CREATE TABLE group_data (
    chat_id BIGINT PRIMARY KEY,
    owner_guid VARCHAR(64) NOT NULL,
    start_time DOUBLE PRECISION DEFAULT 0,
    is_vip BOOLEAN DEFAULT FALSE
);
CREATE TABLE group_permissions (
    chat_id BIGINT PRIMARY KEY,
    change_info BOOLEAN DEFAULT TRUE,
    pin_message BOOLEAN DEFAULT TRUE,
    delete_message BOOLEAN DEFAULT TRUE,
    delete_member BOOLEAN DEFAULT TRUE,
    add_admin BOOLEAN DEFAULT TRUE,
    change_acc BOOLEAN DEFAULT TRUE,

    CONSTRAINT fk_permissions_group
        FOREIGN KEY (chat_id)
        REFERENCES group_data(chat_id)
        ON DELETE CASCADE
);
CREATE TABLE group_admins (
    id BIGSERIAL PRIMARY KEY,
    chat_id BIGINT NOT NULL,
    user_guid VARCHAR(64) NOT NULL,

    CONSTRAINT fk_admins_group
        FOREIGN KEY (chat_id)
        REFERENCES group_data(chat_id)
        ON DELETE CASCADE,

    CONSTRAINT uq_admin_unique
        UNIQUE (chat_id, user_guid)
);
CREATE TABLE group_filters (
    id BIGSERIAL PRIMARY KEY,
    chat_id BIGINT NOT NULL,
    filters TEXT NOT NULL,

    CONSTRAINT fk_filters_group
        FOREIGN KEY (chat_id)
        REFERENCES group_data(chat_id)
        ON DELETE CASCADE
);
CREATE TABLE group_blocked_contracts (
    id BIGSERIAL PRIMARY KEY,
    chat_id BIGINT NOT NULL,
    blocked_contract TEXT NOT NULL,

    CONSTRAINT fk_blocked_contracts_group
        FOREIGN KEY (chat_id)
        REFERENCES group_data(chat_id)
        ON DELETE CASCADE
);


CREATE INDEX idx_admins_chat
ON group_admins(chat_id);

CREATE INDEX idx_filters_chat
ON group_filters(chat_id);

CREATE INDEX idx_blocked_chat
ON group_blocked_contracts(chat_id);
