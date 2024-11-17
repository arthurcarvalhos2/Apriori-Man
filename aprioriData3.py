using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Accord.MachineLearning.Rules;

class Program
{
    static void Main()
    {
        string filePath = "./data/data3.csv";

        Console.WriteLine("Linhas brutas do arquivo:");
        using (var reader = new StreamReader(filePath))
        {
            for (int i = 0; i < 5; i++)
            {
                if (reader.EndOfStream) break;
                Console.WriteLine(reader.ReadLine());
            }
        }

        var transactions = new List<string[]>
        {
            new[] { "leite", "manteiga", "pão" },
            new[] { "pão", "manteiga" },
            new[] { "leite", "pão" },
            new[] { "leite", "manteiga" }
        };

        var allItems = transactions.SelectMany(t => t).Distinct().OrderBy(i => i).ToList();
        var binaryMatrix = transactions.Select(transaction =>
            allItems.Select(item => transaction.Contains(item) ? 1 : 0).ToArray()).ToArray();

        Console.WriteLine("\nMatriz binária das transações:");
        foreach (var row in binaryMatrix)
        {
            Console.WriteLine(string.Join(", ", row));
        }

        var apriori = new Apriori(threshold: 0.5, confidence: 0.5);
        var results = apriori.Learn(transactions.ToArray());

        Console.WriteLine("\nRegras de Associação com Suporte 50% e Confiança 50%:");
        foreach (var rule in results.Rules)
        {
            Console.WriteLine($"{string.Join(", ", rule.X)} => {string.Join(", ", rule.Y)} (Suporte: {rule.Support:F2}, Confiança: {rule.Confidence:F2})");
        }

        apriori = new Apriori(threshold: 0.5, confidence: 0.75);
        results = apriori.Learn(transactions.ToArray());

        Console.WriteLine("\nRegras de Associação com Suporte 50% e Confiança 75%:");
        foreach (var rule in results.Rules)
        {
            Console.WriteLine($"{string.Join(", ", rule.X)} => {string.Join(", ", rule.Y)} (Suporte: {rule.Support:F2}, Confiança: {rule.Confidence:F2})");
        }
    }
}