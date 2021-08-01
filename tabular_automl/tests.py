import unittest

import pandas as pd

from .settings import DATA_DIR
from .tabular_automl import TabularAutoML


class TabularAutoMLTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data_path = DATA_DIR / "titanic"
        cls.train_data_path = cls.data_path / "train.csv"
        cls.index_col = "PassengerId"
        cls.target_col = "Survived"
        cls.task_type = "classification"

    def test_validate_file_path(self):
        # not a Path
        with self.assertRaises(ValueError):
            TabularAutoML("not_a_path")

        # non-existent path
        with self.assertRaises(ValueError):
            TabularAutoML(self.data_path / "does_not_exist.csv")

        # unsupported format
        with self.assertRaises(ValueError):
            TabularAutoML(self.data_path / "titanic.zip")

    def test_get_module(self):
        with self.assertRaises(ValueError):
            TabularAutoML(self.train_data_path, target_col=self.target_col)

        with self.assertRaises(ValueError):
            TabularAutoML(
                self.train_data_path, target_col=self.target_col, task_type="unknown"
            )

    def test_get_data(self):
        with self.assertRaises(ValueError):
            TabularAutoML(
                self.train_data_path,
                index_col="unknown",
                target_col=self.target_col,
                task_type=self.task_type,
            )

        with self.assertRaises(ValueError):
            TabularAutoML(
                self.train_data_path,
                index_col=self.index_col,
                target_col="unknown",
                task_type=self.task_type,
            )

        automl = TabularAutoML(
            self.train_data_path,
            index_col=self.index_col,
            target_col=self.target_col,
            task_type=self.task_type,
        )
        self.assertTrue(isinstance(automl.train_data, pd.DataFrame))

    def testget_sample(self):
        automl = TabularAutoML(
            self.train_data_path,
            index_col=self.index_col,
            target_col=self.target_col,
            task_type=self.task_type,
        )
        sample = automl.get_sample()
        sample_frac = sample.shape[0] / automl.train_data.shape[0]
        self.assertGreaterEqual(sample_frac, 0.5)

    def test_setup(self):
        self.assertTrue(True)

    def test_compare_models(self):
        self.assertTrue(True)

    def test_get_best_model(self):
        automl = TabularAutoML(
            self.train_data_path,
            index_col=self.index_col,
            target_col=self.target_col,
            task_type=self.task_type,
        )
        config = {"setup": dict(silent=True)}
        automl.get_best_model(config)


if __name__ == "__main__":
    unittest.main()
