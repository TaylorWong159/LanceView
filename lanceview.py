"""
LanceDB Viewer
"""

import os

import lancedb
import streamlit as st

STORAGE_FILE = os.path.join(os.getcwd(), 'data')
os.makedirs(os.path.dirname(STORAGE_FILE), exist_ok=True)


class Storage:
    """
    Key-Value Store backed by local file storage.
    """
    def __init__(self, storage_file: str):
        self._storage_file = storage_file
        self._store: dict[str, str] = {}
        self.load()

    def load(self) -> None:
        """
        Load the store from the storage file.
        """
        if os.path.exists(self._storage_file):
            with open(self._storage_file, 'r', encoding='utf-8') as f:
                for line in f:
                    key, value = line.strip().split('=', 1)
                    self._store[key] = value

    def save(self):
        """
        Save the store to the storage file.
        """
        with open(self._storage_file, 'w', encoding='utf-8') as f:
            for key, value in self._store.items():
                f.write(f"{key}={value}\n")

    def __setitem__(self, key: str, value: str):
        self._store[key] = value
        self.save()

    def get[T](self, key: str, default: T = None) -> (str | T):
        """
        Get a value from the store by key.
        If the key does not exist, return the default value.

        Args:
            key (str): The key to retrieve.
            default (T, optional): The default value to return if the key does not exist. Defaults
                to None.

        Returns:
            str | T: The value associated with the key, or the default value if the key does not
                exist in the store.
        """
        return self._store.get(key, default)

    def __getitem__(self, key: str) -> str:
        return self._store[key]

    def __delitem__(self, key: str):
        del self._store[key]
        self.save()

    def __str__(self) -> str:
        return f'Storage(file={self._storage_file}, store={self._store})'

def main():
    """
    Main function to run the LanceDB Viewer application.
    """
    storage = Storage(STORAGE_FILE)
    print(storage)
    st.title("LanceDB Viewer")
    st.set_page_config(
        page_title="LanceDB Viewer",
        page_icon=":mag_right:",
        layout="wide",
    )
    database_uri_input = st.text_input(
        label="Enter the LanceDB URI",
        placeholder="lancedb://path/to/your/database",
        value=storage.get('database_uri', ''),
    )
    if database_uri_input:
        storage['database_uri'] = database_uri_input
        db = lancedb.connect(database_uri_input)
        st.write(f"Connected to database at: {database_uri_input}")
        tables: list[str] = list(db.table_names())
        selected_table = storage.get('selected_table', None)
        index = 0
        if selected_table is not None:
            try:
                index = tables.index(selected_table)
            except ValueError:
                ...
        table = st.selectbox(
            label="Select a table to view",
            index=index,
            options=tables,
        )
        if table:
            storage['selected_table'] = table
            st.write(f"Table: {table}")
            table_data = db[table].to_pandas()
            st.dataframe(table_data)

if __name__ == "__main__":
    main()
