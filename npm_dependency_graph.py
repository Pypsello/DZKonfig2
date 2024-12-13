import os
import json
import toml
from graphviz import Digraph
import matplotlib.pyplot as plt

class NpmDependencyGraph:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.dependencies = {}

    def load_config(self, config_path):
        with open(config_path, 'r') as f:
            return toml.load(f)

    def get_package_json(self):
        package_json_path = os.path.join(self.config['package']['path'], 'package.json')
        if not os.path.isfile(package_json_path):
            raise FileNotFoundError(f"Файл package.json не найден в репозитории: {self.config['package']['path']}")
        with open(package_json_path, 'r') as f:
            return json.load(f)

    def collect_dependencies(self):
        package_json = self.get_package_json()
        dependencies = package_json.get('dependencies', {})
        dev_dependencies = package_json.get('devDependencies', {})
        self.dependencies = {**dependencies, **dev_dependencies}
        return True

    def build_graph(self):
        print("Создание графа зависимостей...")
        dot = Digraph(comment="Npm Dependency Graph")

        # Добавляем узлы в граф
        for package in self.dependencies:
            dot.node(package, package)

        # Добавляем направленные ребра для обозначения зависимостей
        for package in self.dependencies:
            for dependency in self.dependencies:
                if package != dependency:
                    dot.edge(package, dependency, dir='both', style='dashed')

        # Выводим график на экран
        dot.format = 'png'
        dot.render('dependency_graph', view=True)

    def generate_dependency_graph(self):
        if self.collect_dependencies():
            print(f"Зависимости успешно собраны. Создаём граф...")
            self.build_graph()
        else:
            print("Не удалось создать граф зависимостей.")


def test_npm_dependency_graph():
    config_path = 'config.toml'
    graph = NpmDependencyGraph(config_path)
    graph.generate_dependency_graph()


if __name__ == "__main__":
    test_npm_dependency_graph()
