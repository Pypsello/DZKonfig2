import os
import unittest
import json
import toml
from unittest.mock import patch, mock_open, MagicMock
from npm_dependency_graph import NpmDependencyGraph


class TestNpmDependencyGraph(unittest.TestCase):

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.test_config_path = 'test_config.toml'
        self.test_package_json_path = 'test_package.json'

        self.test_config_content = """
            [package]
            path = "."
        """
        with open(self.test_config_path, 'w', encoding='utf-8') as f:
            f.write(self.test_config_content)

        self.test_package_json_content = {
            "name": "example-package",
            "version": "1.0.0",
            'dependencies': {
                'package1': '^1.0.0',
                'package2': '^2.0.0'
            },
            'devDependencies': {
                'package3': '^3.0.0'
            }
        }
        with open(self.test_package_json_path, 'w', encoding='utf-8') as f:
            json.dump(self.test_package_json_content, f)

    def tearDown(self):
        if os.path.exists(self.test_config_path):
            os.remove(self.test_config_path)
        if os.path.exists(self.test_package_json_path):
            os.remove(self.test_package_json_path)

    def test_load_config(self):
        """Простая проверка загрузки конфигурации"""
        graph = NpmDependencyGraph(self.test_config_path)
        self.assertTrue(isinstance(graph.config, dict))

    def test_get_package_json(self):
        """Простая проверка загрузки package.json"""
        graph = NpmDependencyGraph(self.test_config_path)
        try:
            package_json = graph.get_package_json()
            self.assertTrue(isinstance(package_json, dict))
        except FileNotFoundError:
            self.fail("FileNotFoundError при загрузке package.json")

    def test_collect_dependencies(self):
        """Простая проверка сбора зависимостей"""
        graph = NpmDependencyGraph(self.test_config_path)
        try:
            result = graph.collect_dependencies()
            self.assertTrue(result)
            self.assertTrue(isinstance(graph.dependencies, dict))
        except FileNotFoundError:
            self.fail("FileNotFoundError при сборе зависимостей")

    def test_build_graph(self):
        """Простая проверка построения графа"""
        graph = NpmDependencyGraph(self.test_config_path)
        graph.dependencies = {'package1': '1.0.0'}
        try:
            graph.build_graph()
        except Exception as e:
            self.fail(f"build_graph вызвала исключение: {e}")

    def test_generate_dependency_graph(self):
        """Простая проверка генерации графа"""
        graph = NpmDependencyGraph(self.test_config_path)
        try:
            graph.generate_dependency_graph()
        except Exception as e:
            self.fail(f"generate_dependency_graph вызвала исключение: {e}")

    def test_get_package_json_file_not_found(self):
        """Проверка исключения при отсутствии package.json"""
        graph = NpmDependencyGraph('config.toml')
        with self.assertRaises(FileNotFoundError):
            graph.get_package_json()


if __name__ == "__main__":
    unittest.main()